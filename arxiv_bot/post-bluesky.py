#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText
#%%
def main(today:str, categories_content):
    printlog('Start posting on Bluesky')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
    printlog(f"This is the end of all the posts on {today}")

    return 0

if __name__ == '__main__':
    # date = '2024-08-09'
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content)

# %%
