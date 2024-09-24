#%%
from src.utils.get_args import html_args, get_today, categories_content
from src.core.arxiv_function import ArxivSearch, ArxivText
from src.core.printlog import printlog
#%%
def save_html_json(today):
    args = html_args()
    for category in categories_content:
        # save_html()
        search = ArxivSearch(category, args.submissions, args.skip, args.show)
        search.save_one_html()
        # save_json()
        data = ArxivText(category, today, extension='.json')
        data.save_one_json()
    return 0

def post_bluesky(today):
    for category in reversed(categories_content):
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
def post_twitter(today, twi = 5):
    for category in reversed(categories_content[:twi]):
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    return 0

def main():
    today = get_today()    
    # save_html_json(today)
    # post_bluesky(today)
    post_twitter(today, twi = 3)
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    main()