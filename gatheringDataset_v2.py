from googlesearch import search
from datetime import date, timedelta 
import httplib2
import pandas as pd
from urllib.parse import urlencode
import newspaper
from newspaper import Article, Config, news_pool
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
    era = (startDate-endDate).days
    ua = UserAgent()
    #configurating newspaper
    config = Config()
    config.memoize_articles = False
    config.request_timeout = 8

    currentDate = startDate
    df_tofill = pd.DataFrame({'A' : []})
    while currentDate < endDate:
        tbs = get_tbs(currentDate,currentDate+period)
        #listSources = ['https://www.fxempire.com/']
        urls = list( search(searchQuery, stop=articlesPerPeriod, pause=25.0,
                tpe = 'nws', tbs = tbs, user_agent = ua.random ) )    # domains = listSources
                
        dates = [currentDate] * len(urls)
        articles = [Article(url, config=config) for url in urls]    
        news_pool.set(articles, threads_per_source=2)
        news_pool.join()  
               
        for i,article in enumerate(articles):
            try:
                article.parse()
            except:
                continue
                      
            if article.meta_lang != 'en':
                continue

            localFrame = pd.DataFrame({
                'date':dates[i],
                'url':urls[i],
                'text':article.text
            }, index=[0])
            if df_tofill.empty:
                df_tofill = localFrame
            else:
                
                df_tofill = df_tofill.append(localFrame, ignore_index=True)
            pass

        currentDate += period + timedelta(days=1)
        print(f'complete: {100*(startDate-currentDate).days/era} percent')
        pass
    
    return df_tofill

searchQuery = 'eurusd forex'
startDate=date(2015,1,1)
peridDays = 2

endDate = date(2015,1,2)
articlesPerPeriod = 5

timeDelta = timedelta(days=peridDays-1)
data_fr = fill_frame(searchQuery,startDate, endDate, timeDelta, articlesPerPeriod)
data_fr.to_excel('15_16_usdeur.xlsx', sheet_name='Sheet1')


