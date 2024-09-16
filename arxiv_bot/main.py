#%%
from get_args import html_args, get_today
from arxiv_function import ArxivSearch, ArxivText, categories_content
from printlog import printlog

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

def post(today):
    twi = 5
    for category in reversed(categories_content):
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
    for category in reversed(categories_content[:twi]):
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    printlog(f"This is the end of all the posts on {today}")
    return 0

def main():
    today = get_today()
    save_html_json(today)
    post(today)
    return 0

if __name__ == '__main__':
    main()