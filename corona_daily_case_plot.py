# HK Govt api.data.gov.hk for source of information
# The purpose is to track confirmed number covid-19 cases in Hong Kong, and also affected flights of confirmed case

import requests                                         #for http requests
from pylab import *                                     #matplotlib
from scipy.ndimage.filters import gaussian_filter1d     #To smooth y axis
import matplotlib.style as style                        #beautify graph
#import mpl_font.wqy                                    #plot with chinese titles


def corona_daily_case_plot():

    style.use('seaborn-poster')                         #sets the style of the charts
    style.use('ggplot')

    #get api dataset
    url = "https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D"
    
    payload = {}
    headers= {}
    numofConfirmedCase=[]
    dates=[]
    daily_corona_case_num = ""      #placeholder for http requested api data
    delta=[]
    previous_cases=0

    daily_corona_case_num = requests.request("GET", url, headers=headers, data = payload).json()

    for i in daily_corona_case_num:
        
        dates.append(i["As of date"])

        if i["Number of confirmed cases"] != '':
            numofConfirmedCase.append(i["Number of confirmed cases"])
            delta.append(int(i["Number of confirmed cases"]) - previous_cases)
            previous_cases = i["Number of confirmed cases"]
        elif i["Number of cases tested positive for SARS-CoV-2 virus by rapid antigen tests"]!= '':
            numofConfirmedCase.append(i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"] + i["Number of cases tested positive for SARS-CoV-2 virus by rapid antigen tests"])
            delta.append(i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"]  + i["Number of cases tested positive for SARS-CoV-2 virus by rapid antigen tests"] - previous_cases)
            previous_cases = i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"]  + i["Number of cases tested positive for SARS-CoV-2 virus by rapid antigen tests"]
        else:
            numofConfirmedCase.append(i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"])
            delta.append(i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"] - previous_cases)
            previous_cases = i["Number of cases tested positive for SARS-CoV-2 virus by nucleic acid tests"]

    #---------- Display latest confirmed covid19 cases and date
    #Get latest number of confirmed case by getting the last entry in the list
    #Get latest date of reported confirmed case by getting the last entry in the list
    daily_num_of_cases = str(numofConfirmedCase[-1]) + "宗"       
    last_update = dates[-1]                                       

    #Prepare x axis date format
    x = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in dates]

    #plot y with smoothed curves style instead of a hard thin line
    ysmoothed = gaussian_filter1d(numofConfirmedCase, sigma=2)
    
    #plot the cumulative confirmed cases against time
    plt.plot(x, ysmoothed)
    grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig('mysite/img/HK_corona_trend.png')
    plt.close()

    #bar chart daily number of cases against time
    plt.bar(x, delta)
    plt.savefig('mysite/img/HK_corona_increment_coloumn_chart.png')
    plt.close()

    return daily_num_of_cases, last_update
