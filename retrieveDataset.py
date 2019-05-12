import pandas as pd
import numpy as np
from datetime import date, timedelta 

startDate=date(2015,1,1)
peridDays = 2

endDate = date(2016,1,1)

print((endDate-startDate).days/peridDays)
