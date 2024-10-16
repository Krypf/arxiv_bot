#%%
from src.utils.printlog import printlog
from src.core.arxiv_function import ArxivText
from src.utils.get_args import categories_content, get_today

#%%
def post_twitter(today, twi = 5):
    for category in reversed(categories_content[:twi]):
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    return 0

def main():
    today = get_today()
    printlog('Start tweeting')
    post_twitter(today)
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    main()