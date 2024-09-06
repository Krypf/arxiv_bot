#%%
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date
from twitter_function import twitter_login, send_post_to_twitter
#%%
def sub(obj: ArxivText, sleep_time=1):
    client = twitter_login(obj.category)
    text = obj.read_content()

    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    d = arxiv_formatted_date(obj.date)
    for t in text_array:
        send_post_to_twitter(client, t, today=d)
        time.sleep(sleep_time)
    printlog(f"This is the end of all the posts on {obj.date}")
    return 0

#%%
def main(today:str, categories_content=categories_content):
    printlog('Start tweeting')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        sub(reader)
    return 0

today = datetime.now().strftime('%Y-%m-%d')
# today = '2024-08-28'
if __name__ == '__main__':
    main(today)

