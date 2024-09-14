#%%
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText
#%%

#%%
def main(today:str, categories_content):
    printlog('Start tweeting')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        reader.update_twitter()
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    # today = '2024-08-28'
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content)

