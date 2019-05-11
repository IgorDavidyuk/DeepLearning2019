from googlesearch import search
from datetime import date, timedelta 
import httplib2
import pandas as pd
from urllib.parse import urlencode
#import pillow
from newspaper import Article
from fake_useragent import  UserAgent

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

def fill_frame(searchQuery, startDate, endDate, period=0, articlesPerPeriod=5):
    '''
    Input:
    searchQuery - string query for google news
    startDate - datetime.date to start search from
    period - timedelta days
    articlesPerPeriod - number of first search results to save

    Output:
    pandas dataframe with columns ()
    '''
    ua = UserAgent()
    currentDate = startDate
    df_tofill = pd.DataFrame({'A' : []})
    while currentDate < endDate:
        tbs = get_tbs(currentDate,currentDate+period)
        #listSources = ['https://www.fxempire.com/']
        for url in search(searchQuery, stop=articlesPerPeriod, pause=15.0,
         tpe = 'nws', tbs = tbs, user_agent = ua.random ):    # domains = listSources
            h = httplib2.Http()
            resp = h.request(url, 'HEAD')
            if int(resp[0]['status']) >= 400:
                continue
                
            article = Article(url)
            article.download()
            article.parse()
            parseDate = article.publish_date
            #print(parseDate)
            if parseDate and currentDate <= parseDate.date() <= currentDate +period:
                articleDate = parseDate
            else:
                articleDate = currentDate
            
            '''article.nlp()
            if article.meta_lang == 'en':
                pass'''

            localFrame = pd.DataFrame({
                'date':articleDate,
                'url':url,
                'text':article.text
            }, index=[0])
            if df_tofill.empty:
                df_tofill = localFrame
            else:
                
                df_tofill = df_tofill.append(localFrame, ignore_index=True)
            pass

        currentDate += period + timedelta(days=1)
        pass
    
    return df_tofill

searchQuery = 'eurusd forex'
startDate=date(2018,6,1)
peridDays = 3

endDate = date(2018,6,30)
articlesPerPeriod = 5

timeDelta = timedelta(days=peridDays-1)
data_fr = fill_frame(searchQuery,startDate, endDate, timeDelta, articlesPerPeriod)
data_fr.to_excel('june2018.xlsx', sheet_name='Sheet1')


