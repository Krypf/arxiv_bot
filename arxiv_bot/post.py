#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from printlog import printlog
from arxiv_function import ArxivText, categories_content, get_today
#%%
def sub(obj: ArxivText):

    obj.update_bluesky()
    
    obj.update_twitter()

    return None

def main():
    today = get_today()
    for category in categories_content[:1]:
        reader = ArxivText(category, today, extension='.json')
        sub(reader)
    printlog(f"This is the end of all the posts on {today}")

    return 0

#%%
if __name__ == '__main__':
    main()
    
# %%
