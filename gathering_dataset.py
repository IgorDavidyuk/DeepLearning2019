from datetime import date, timedelta 
import pandas as pd
from support_dataset import parse_urls, google_links

searchQuery = 'crude oil price forecast' #'crude oil price forecast'
startDate=date(2015,1,10)
periodDays = 4
endDate = date(2019,5,11)
articlesPerPeriod = 10
timeDelta = timedelta(days=periodDays-1)

name = f'{searchQuery.split()[0]}_{searchQuery.split()[1]}_{str(startDate)}_to_{str(endDate)}'

url_fr = google_links(searchQuery,startDate, endDate, timeDelta, articlesPerPeriod)
url_fr.to_excel(f'{name}.xlsx', sheet_name='URLS')

#url_fr = pd.read_excel(f'{name}_URLS.xlsx', 'Sheet1', index_col = 0, na_values=['NA'])
parsed_frame = parse_urls(url_fr)
with pd.ExcelWriter(f'{name}.xlsx', mode='a') as writer:
    parsed_frame.to_excel(writer, sheet_name='PARSED')

