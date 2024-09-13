#%%
from arxiv_func_test import fetch_arxiv
#%%
import sys
from datetime import datetime, timedelta
#%%
def date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)
#%% constants
category = sys.argv[1]

# Define the start and end dates
start_date = datetime.strptime(sys.argv[2], '%Y-%m-%d')
end_date = datetime.strptime(sys.argv[3], '%Y-%m-%d')

# Create the date range iterator
date_iterator = date_range(start_date, end_date)

# Run the script for the dates in the range.
for date in date_iterator:
    date = date.strftime('%Y-%m-%d')
    fetch_arxiv(category, date, __max_results=200)
