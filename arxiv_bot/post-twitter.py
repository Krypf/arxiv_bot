#%%
import time
from datetime import datetime

from printlog import printlog
from arxiv_function import categories_content, ArxivText, arxiv_formatted_date
from twitter_function import login_twitter, send_post_to_twitter
#%%
def sub(obj: ArxivText, sleep_time=1, api_maximum=50):
    client = login_twitter(obj.category)

    # Split the text using "----" as the delimiter
    text = obj.read_content()
    text_array = text.split("\n----\n")
    
    d = arxiv_formatted_date(obj.date)
    for t in text_array:
        send_post_to_twitter(client, t, today=d)
        time.sleep(sleep_time)
    return 0

#%%
def main(today:str, categories_content=categories_content):
    printlog('Start tweeting')
    for category in categories_content:
        printlog(f"The category is {category}")
        reader = ArxivText(category, today)
        sub(reader)
    printlog(f"This is the end of all the posts on {today}")
    return 0

# today = '2024-08-28'
if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    main(today)

