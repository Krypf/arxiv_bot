#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date
from bluesky_function import login_bsky, send_post_to_bluesky
#%%
def sub(obj: ArxivText, sleep_time=1):
    client, thumb = login_bsky(obj.category)
    text = obj.read_content()
    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    d = arxiv_formatted_date(obj.date)
    for t in text_array:
        send_post_to_bluesky(client, t, thumb, today=d)
        time.sleep(sleep_time)
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
    
#%% manual
# category = 'gr-qc'
# date = '2024-08-09'
# obj = reader = ArxivText(category, today)
# text = obj.read_content()

# text_array = text.split("\n----\n")
# client, thumb = login_bsky(category)
# t = text_array[-1]
# send_post_to_bluesky(client, t, thumb)

# %%
