#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText
from bluesky_function import bsky_login, send_post_to_bluesky
#%%
def main(obj: ArxivText, sleep_time=1):
    client, thumb = bsky_login(obj.category)
    text = obj.read_content()
    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    for t in text_array:
        send_post_to_bluesky(client, t, thumb)
        time.sleep(sleep_time)    
    printlog(f"This is the end of all the posts on {obj.date}")
    return 0
#%%
today = datetime.now().strftime('%Y-%m-%d')
# date = '2024-08-09'
if __name__ == '__main__':
    printlog('Start posting on Bluesky')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        main(reader)

#%% manual
# category = 'gr-qc'
# date = '2024-08-09'
# obj = reader = ArxivText(category, today)
# text = obj.read_content()

# text_array = text.split("\n----\n")
# client, thumb = bsky_login(category)
# t = text_array[-1]
# send_post_to_bluesky(client, t, thumb)

# %%
