#%%
from datetime import datetime
from arxiv_function import categories_content, fetch_arxiv

#%% constants

today = datetime.now().strftime('%Y-%m-%d')

# Run scripts

def main():
    for category in categories_content:
        fetch_arxiv(category, today, __max_results = 200)
    return 0

main()
#%%
