#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date
from bluesky_function import bsky_login, send_post_to_bluesky
from twitter_function import twitter_login, Twitter_with_api_max
#%%
def sub(obj: ArxivText, sleep_time=1):
    client_bsky, thumb = bsky_login(obj.category)
    client_twitter = twitter_login(obj.category)
    # Split the text using "----" as the delimiter
    text = obj.read_content()
    text_array = text.split("\n----\n")
    d = arxiv_formatted_date(obj.date)
    iteration = 0
    for t in text_array:
        send_post_to_bluesky(client_bsky, t, thumb, today=d)
        time.sleep(sleep_time)
        iteration += 1
        Twitter_with_api_max(iteration, client_twitter, t, d)
        time.sleep(sleep_time)
        
    return 0

def main(today: str, categories_content=categories_content):
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        sub(reader, sleep_time = 0.5)
    printlog(f"This is the end of all the posts on {today}")

    return 0

#%%
if __name__ == '__main__':
    # today = datetime.now().strftime('%Y-%m-%d')
    # today = '2024-09-04'
    today = '2024-09-05'
    main(today)
    
# %%
