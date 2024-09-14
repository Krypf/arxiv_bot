#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, ArxivPost
from bluesky_function import login_bsky, Bluesky
#%%
def update_bluesky(obj: ArxivText, sleep_time=1):
    articles_list = obj.read_content()
    client_bsky, thumb = login_bsky(obj.category)
    for article in articles_list:
        article = Bluesky(article)
        article.send_post_to_bluesky(client_bsky, thumb)
        time.sleep(sleep_time)
    client_bsky.send_post(obj.last_post())
    return None
#%%
def main(today:str, categories_content):
    printlog('Start posting on Bluesky')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        update_bluesky(reader)
    printlog(f"This is the end of all the posts on {today}")

    return 0

if __name__ == '__main__':
    # date = '2024-08-09'
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content)
    

# %%
