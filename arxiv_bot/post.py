#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, ArxivPost
from bluesky_function import login_bsky, Bluesky
from twitter_function import login_twitter, Twitter
#%%
def sub(obj: ArxivText, sleep_time=1):
    articles_list = obj.read_content()
    client_bsky, thumb = login_bsky(obj.category)
    client_twitter = login_twitter(obj.category)
    # Bluesky
    # for article in articles_list:
    #     article = Bluesky(article)
    #     article.send_post_to_bluesky(client_bsky, thumb)
    #     time.sleep(sleep_time)
    # client_bsky.send_post(obj.last_post())
    # Twitter
    for article in articles_list:
        article = Twitter(article)
        twi_api = article.send_post_to_twitter(client_twitter)
        if twi_api:
            api_maximum = 50
            t = f"Twitter API v2 limits posts to 1500 per month ({api_maximum} per day). All the posts including the remaining submissions are posted on Bluesky: " + f"https://bsky.app/profile/krxiv-{obj.category}.bsky.social"
            printlog(f"Stop sending tweets. Please tweet manually:\n{t}")
            break
        time.sleep(sleep_time)
    client_twitter.create_tweet(text=obj.last_post())
    
    return None

def main(today: str, categories_content):
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        sub(reader, sleep_time = 0.5)
    printlog(f"This is the end of all the posts on {today}")

    return 0

#%%
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    today = '2024-09-13'
    main(today, categories_content[:1])
    
# %%
