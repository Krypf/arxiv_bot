#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date, ArxivPost, post_last
from bluesky_function import login_bsky, send_post_to_bluesky
#%%
def sub(obj: ArxivText, sleep_time=1):
    client_bsky, thumb = login_bsky(obj.category)
    articles_list = ArxivPost(obj.read_content())
    d = arxiv_formatted_date(obj.date)
    # Bluesky
    for article in articles_list:
        printlog(f"Target article: {article.title}")
        article.send_post_to_bluesky(client_bsky, thumb)
        time.sleep(sleep_time)
    client_bsky.send_post(post_last(d))
    return 0
#%%
def main(today:str, categories_content=categories_content):
    printlog('Start posting on Bluesky')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        sub(reader)
    printlog(f"This is the end of all the posts on {today}")

    return 0

# date = '2024-08-09'
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    main(today)
    

# %%
