# -*- coding: utf-8 -*-
import requests

from pylab import * #matplotlib
from scipy.ndimage.filters import gaussian_filter1d #To smooth y axis
import matplotlib.style as style #beautify graph
#import mpl_font.wqy #plot with chinese titles


def corona_daily_case_plot():

    style.use('seaborn-poster') #sets the style of the charts
    style.use('ggplot')

    url = "https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D"
    payload = {}
    headers= {}
    i=0
    y=[]
    dates=[]
    daily_corona_case_num = ""
    delta=[]
    previous_cases=0

    daily_corona_case_num = requests.request("GET", url, headers=headers, data = payload).json()

    for i in daily_corona_case_num:
        dates.append(i["As of date"])
        y.append(i["Number of confirmed cases"])
        delta.append(i["Number of confirmed cases"] - previous_cases)
        previous_cases = i["Number of confirmed cases"]
#

    daily_num_of_cases = str(y[-1]) + "宗"
    last_update = dates[-1]

    x = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in dates]
#    plottitle = "Confirmed Convid-19 Cases - HK Daily Trend" + "\n" + dates[-1] + " : " + str(y[-1]) + " Cases"

    ysmoothed = gaussian_filter1d(y, sigma=2)
    plt.plot(x, ysmoothed)
    grid(True)
    #suptitle('cakwok')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    #plt.show()
    plt.savefig('mysite/img/HK_corona_trend.png')
    plt.close()

    plt.bar(x, delta)
    plt.savefig('mysite/img/HK_corona_increment_coloumn_chart.png')
    plt.close()

    return daily_num_of_cases, last_update

