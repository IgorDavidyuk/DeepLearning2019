from googlesearch import search
from datetime import date, timedelta 
import pandas as pd
from urllib.parse import urlencode
#import pillow
from newspaper import Article
from fake_useragent import  UserAgent

ua = UserAgent()

def get_tbs(fromDate, toDate):
    """ return google search tbs parameter for date range

    :param fromDate: python date
    :param toDate:   python date
    :return:  tbs urlencoded value (excluding tbs=)
    """
    # dates to m/d/yyyy format
    fromDate = fromDate.strftime("%m/%d/%Y")
    toDate = toDate.strftime("%m/%d/%Y")
    return urlencode(dict(tbs=f"cdr:1,cd_min:{fromDate},cd_max:{toDate}"))[4:]

searchQuery = 'eurusd forex'
startDate=date(2017,11,15)
timeDelta = timedelta(days=1)
endDate = startDate + timeDelta
articlesPerPeriod = 5

tbs = get_tbs(startDate,endDate)
#listSources = ['https://www.fxempire.com/']
for url in search(searchQuery, stop=articlesPerPeriod, pause=22.0, tpe = 'nws', tbs = tbs, user_agent = ua.random ):    # domains = listSources
    print(url)
    article = Article(url)
    article.download()
    article.parse()
    print(article.text)
