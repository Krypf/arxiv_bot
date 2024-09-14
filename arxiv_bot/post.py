#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText
#%%
def sub(obj: ArxivText):

    obj.update_bluesky()
    
    obj.update_twitter()

    return None

def main(today: str, categories_content):
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        sub(reader)
    printlog(f"This is the end of all the posts on {today}")

    return 0

#%%
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    today = '2024-09-13'
    main(today, categories_content[:1])
    
# %%
