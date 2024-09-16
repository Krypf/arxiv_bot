#%%
from printlog import printlog
from arxiv_function import categories_content, ArxivText
from get_args import get_today

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
