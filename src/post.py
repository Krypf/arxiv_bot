#%%
from core.printlog import printlog
from core.arxiv_function import ArxivText
from utils.get_args import get_today, categories_content

def post():
    today = get_today()
    twi = 5
    for category in reversed(categories_content):
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
    for category in reversed(categories_content[:twi]):
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    printlog(f"This is the end of all the posts on {today}")
    return 0

main = post

if __name__ == '__main__':
    main()
    
# %%
