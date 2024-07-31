#%% https://chatgpt.com/c/7e987fc0-91b5-4240-881b-df03af053070
import sys
import os

# Get the current directory of the test script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the arxiv_bot folder
arxiv_bot_dir = os.path.join(current_dir, '..', 'arxiv_bot')

# Add the arxiv_bot folder to the system path
sys.path.insert(0, arxiv_bot_dir)

# Now you can import the module
import arxiv_function
#%%
from datetime import datetime, timedelta

def date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)
#%% constants
category = 'gr-qc'

# Define the start and end dates
start_date = datetime.strptime('2024-07-22', '%Y-%m-%d')
end_date = datetime.strptime('2024-07-31', '%Y-%m-%d')

# Create the date range iterator
date_iterator = date_range(start_date, end_date)

# Run the script for the dates in the range.
for date in date_iterator:
    date = date.strftime('%Y-%m-%d')
    arxiv_function.fetch_arxiv(category, date)
