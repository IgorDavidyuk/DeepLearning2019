from googlesearch import search
from datetime import date, timedelta 
import httplib2
import pandas as pd
from urllib.parse import urlencode
import newspaper
from newspaper import Article, Config, news_pool
from fake_useragent import  UserAgent
from tqdm.autonotebook import tqdm, trange

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

def google_links(searchQuery, startDate, endDate, period=0, articlesPerPeriod=5):
    '''
    Function googles links
    Input:
    searchQuery - string query for google news
    startDate - datetime.date to start search from
    period - timedelta days
    articlesPerPeriod - number of first search results to save

    Output:
    pandas dataframe (dates, urls)
    '''
    ua = UserAgent()
    urls = []
    dates = []
    currentDate = startDate
    era = (endDate + period - startDate).days
    while currentDate < endDate:
        tbs = get_tbs(currentDate,currentDate+period)
        #listSources = ['https://www.fxempire.com/']
        local_urls = list( search(searchQuery, stop=articlesPerPeriod, pause=12.0,
                tpe = 'nws', tbs = tbs, user_agent = ua.random ) )    # domains = listSources 
        
        urls.extend( local_urls )
        dates.extend( [currentDate] * len(local_urls) )
        
        currentDate += period + timedelta(days=1)
        print(f'complete: {round(100*(currentDate-startDate).days/era,2)} %')
        pass
    
    if len(urls) == len(dates):
        pass
    elif len(urls) > len(dates):
        urls = urls[:len(dates)]
    else:
        dates = dates[:len(urls)]
    #IMPLEMENT DIRECT SAVING TO DISK
    df_tofill = pd.DataFrame({'date' : dates,
                              'urls' : urls})
    return df_tofill

def parse_urls(dataframe):
    '''
    Function parses urls feeded
    
    Output:
    pandas dataframe with columns (date, lang, url, text)
    '''    
    #configurating newspaper
    config = Config()
    config.memoize_articles = False
    config.request_timeout = 8

    df_tofill = pd.DataFrame({'A' : []})
    total_articles_saved = 0
   
    dates = dataframe['date'].tolist()
    urls = dataframe['urls'].tolist()

    articles = [Article(url, config=config) for url in urls]
    news_pool.set(articles, override_threads=50)
    news_pool.join()      
    
    given_articles = len(dates)      
    for i,article in enumerate(tqdm(articles, desc='parsing')):
        #if i%10 == 0:
            #print(f'parsing complete: {round(100*i/given_articles, 2)} %')
        try:
            article.parse()
        except:
            continue
        
        if article.meta_lang == 'en':
            pass
        elif article.meta_lang == '':
            pass
        else:            
            continue
        
        total_articles_saved +=1
        localFrame = pd.DataFrame({
            'date':dates[i],
            'lang':article.meta_lang,
            'url':urls[i],
            'text':article.text
        }, index=[0])
        if df_tofill.empty:
            df_tofill = localFrame
        else:            
            df_tofill = df_tofill.append(localFrame, ignore_index=True)
        pass
    
     
    print(f"total articles parsed: {given_articles}; articles accepted: {total_articles_saved}")
    return df_tofill

''''''


