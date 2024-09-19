#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from core.printlog import printlog
from arxiv_function import ArxivText
from utils.get_args import get_today, categories_content

#%%
def main():
    today = get_today()
    
    printlog('Start posting on Bluesky')
    for category in categories_content:
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
    printlog(f"This is the end of all the posts on {today}")
    
    return 0

if __name__ == '__main__':
    main()

# %%
