#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import os
import time
from datetime import datetime

from bluesky_function import read_text_file, bsky_login, send_post_to_bluesky
from printlog import printlog
from arxiv_function import categories_content
#%%
def main(category, date, sleep_time=1):
    client, thumb = bsky_login(category)
    text = read_text_file(category, date, parent_folder=os.path.expanduser("~/arxiv_bot"))
    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    for t in text_array:
        send_post_to_bluesky(client, t, thumb)
        time.sleep(sleep_time)    
    return 0
#%%

today = datetime.now().strftime('%Y-%m-%d')
# date = '2024-08-09'

if __name__ == '__main__':
    for category in categories_content:
        printlog(f"The category is {category}")
        main(category, today)
    printlog(f"This is the end of all the posts on {today}")

#%% manual
# category = 'gr-qc'
# date = '2024-08-09'
# text = read_text_file(category, date, parent_folder=os.path.expanduser("~/arxiv_bot"))
# text_array = text.split("\n----\n")
# client, thumb = bsky_login(category)
# t = text_array[-1]
# send_post_to_bluesky(client, t, thumb)

# %%
