from datetime import date, timedelta 
import pandas as pd
from support_dataset import parse_urls, google_links

searchQuery = 'eurusd forex'
startDate=date(2015,1,1)
peridDays = 5
endDate = date(2015,1,11)
articlesPerPeriod = 8
timeDelta = timedelta(days=peridDays-1)

name = f'{searchQuery.split()[0]}_{searchQuery.split()[1]}_{str(startDate)}_to_{str(endDate)}'

url_fr = google_links(searchQuery,startDate, endDate, timeDelta, articlesPerPeriod)
url_fr.to_excel(f'{name}.xlsx', sheet_name='URLS')

#url_fr = pd.read_excel(f'{name}_URLS.xlsx', 'Sheet1', index_col = 0, na_values=['NA'])
parsed_frame = parse_urls(url_fr)
with pd.ExcelWriter(f'{name}.xlsx', mode='a') as writer:
    parsed_frame.to_excel(writer, sheet_name='PARSED')

