#def do_calculation(number1, number2):
#    return number1 + number2
import requests

def do_calculation(flightnumber, lang):
    if lang == "c":
       url = "https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fflights_trains_list_chi.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22eq%22%2C%5B%22" + flightnumber + "%22%5D%5D%5D%7D"
    else:
       url = "https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fflights_trains_list_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22ct%22%2C%5B%22" + flightnumber + "%22%5D%5D%5D%7D"
    payload = {}
    headers= {}
    html_body = ""
    i = 0

    # get new corona case from HK govt api
    get_latest_corona_case = requests.request("GET", url, headers=headers, data = payload).json()
    #print(get_latest_corona_case[0])
    for i in get_latest_corona_case:
        for keys, values in i.items():
            html_body += keys + "  :  " + values + "<br>"
        html_body += "<br>"
    if html_body == "":
        if lang == "c":
            html_body = "該航班没有確診個案。"
        else :
            html_body = "There is no confirmed case.  Stay safe."
    return html_body