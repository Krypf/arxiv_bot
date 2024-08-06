#%%
from datetime import datetime
import arxiv_function
#%%
#%% constants
categories_content = arxiv_function.read_categories_file('arxiv_bot')# the current directory is arxiv_bot and the subfolder is arxiv_bot

today = datetime.now().strftime('%Y-%m-%d')

# Run scripts

def main():
    for category in categories_content:
        arxiv_function.fetch_arxiv(category, today, __max_results = 200)
    return 0

main()
#%%
