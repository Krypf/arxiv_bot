#%%
from datetime import datetime
from arxiv_func_test import categories_content, fetch_arxiv

#%%
def main():
    today = datetime.now().strftime('%Y-%m-%d')
    for category in categories_content:
        fetch_arxiv(category, today, __max_results = 200)
    return 0
# Run scripts
main()
#%%
