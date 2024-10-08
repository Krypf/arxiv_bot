#%%
from core.printlog import printlog
from core.arxiv_function import ArxivText
from utils.get_args import categories_content, get_today

#%%
def main():
    today = get_today()
    
    printlog('Start tweeting')
    for category in categories_content:
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    main()
