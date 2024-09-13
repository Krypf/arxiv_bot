#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date
from bluesky_function import login_bsky, send_post_to_bluesky
from twitter_function import login_twitter, send_post_to_twitter
#%%
def sub(obj: ArxivText, sleep_time=1):
    client_bsky, thumb = login_bsky(obj.category)
    client_twitter = login_twitter(obj.category)
    # Split the text using "----" as the delimiter
    text = obj.read_content()
    text_array = text.split("\n----\n")
    d = arxiv_formatted_date(obj.date)
    for t in text_array:
        printlog(f"Target text:\n{t}")
        send_post_to_bluesky(client_bsky, t, thumb, today=d)
        time.sleep(sleep_time)
    for t in text_array:
        printlog(f"Target text:\n{t}")
        twi_api = send_post_to_twitter(client_twitter, t, today = d)
        if twi_api:
            api_maximum = 50
            t = f"Twitter API v2 limits posts to 1500 per month ({api_maximum} per day). All the posts including the remaining submissions are posted on Bluesky: " + f"https://bsky.app/profile/krxiv-{obj.category}.bsky.social"
            printlog(f"Stop sending tweets. Please tweet manually:\n{t}")
            break
        time.sleep(sleep_time)
    return None

def main(today: str, categories_content=categories_content):
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        sub(reader, sleep_time = 0.5)
    printlog(f"This is the end of all the posts on {today}")

    return 0

#%%
if __name__ == '__main__':
    # today = '2024-09-04'
    # today = '2024-09-05'
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content=categories_content)
    
# %%
