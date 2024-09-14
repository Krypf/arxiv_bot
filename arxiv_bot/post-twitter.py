#%%
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText
from twitter_function import login_twitter, Twitter
#%%
def update_twitter(obj: ArxivText, sleep_time=1, api_maximum=50):
    articles_list = obj.read_content()
    client_twitter = login_twitter(obj.category)
    for article in articles_list:
        article = Twitter(article)
        article.send_post_to_twitter(client_twitter)
        time.sleep(sleep_time)
    client_twitter.create_tweet(text=obj.last_post())
    return None

#%%
def main(today:str, categories_content):
    printlog('Start tweeting')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today, extension='.json')
        update_twitter(reader)
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    # today = '2024-08-28'
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content)

