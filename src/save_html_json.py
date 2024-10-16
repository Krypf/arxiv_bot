from src.utils.get_args import get_args, get_today, categories_content
from src.core.arxiv_function import ArxivSearch, ArxivText
#%%
def save_html_json(today, args):
    # be going to change args
    for category in categories_content:
        # save_html
        search = ArxivSearch(category, args.submissions, args.skip, args.show)
        search.save_one_html()
        # save_json
        data = ArxivText(category, today, extension='.json')
        data.save_one_json()
    return 0
#%%
def save_html(args):
    for category in categories_content:
        search = ArxivSearch(category, args.submissions, args.skip, args.show)
        search.save_one_html()
    return 0

def save_json(args):
    today = get_today(args)
    for category in categories_content:
        obj = ArxivText(category, today, extension='.json')
        obj.save_one_json()
    return 0
