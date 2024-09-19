#%% 
from core.arxiv_function import ArxivSearch
from utils.get_args import html_args, categories_content
# from typing import Optional
def save_html():
    args = html_args()
    for category in categories_content:
        search = ArxivSearch(category, args.submissions, args.skip, args.show)
        search.save_one_html()
    return 0

main = save_html
#%%
if __name__ == "__main__":
    main()
