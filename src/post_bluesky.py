#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from src.utils.printlog import printlog
from src.core.arxiv_function import ArxivText
from src.utils.get_args import get_args, get_today, categories_content

#%%
def post_bluesky(today):
    for category in reversed(categories_content):
        reader = ArxivText(category, today, extension='.json')
        reader.update_bluesky()
        
def main():
    args = get_args()
    
    today = get_today(args)
    
    printlog('Start posting on Bluesky')
    post_bluesky(today)
    printlog(f"This is the end of all the posts on {today}")
    
    return 0

if __name__ == '__main__':
    main()

# %%
