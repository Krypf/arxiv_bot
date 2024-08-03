#%%
import sys
from datetime import datetime, timedelta

file_name = 'tests/import_module.py'
with open(file_name, 'r') as file:
    script = file.read()
exec(script)
#%%
# Now you can import the module
import arxiv_function
#%%

def date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)
#%% constants
category = sys.argv[1]

# Define the start and end dates
start_date = datetime.strptime('2024-07-24', '%Y-%m-%d')
end_date = datetime.strptime('2024-07-25', '%Y-%m-%d')

# Create the date range iterator
date_iterator = date_range(start_date, end_date)

# Run the script for the dates in the range.
for date in date_iterator:
    date = date.strftime('%Y-%m-%d')
    arxiv_function.fetch_arxiv(category, date, __max_results=200)
