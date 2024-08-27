#%%
from twitter_function import twitter_login, send_post_to_twitter
from arxiv_function import categories_content
from bluesky_function import read_text_file
import os

#%%
from printlog import printlog
import time
from datetime import datetime
#%%
def main(category, date, sleep_time=1):
    client = twitter_login(category)
    text = read_text_file(category, date, parent_folder=os.path.expanduser("~/arxiv_bot"))
    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    for t in text_array:
        send_post_to_twitter(client, t, thumb)
        time.sleep(sleep_time)    
    return 0

def main(category, date, sleep_time=1):
    
    return 0

main()

#%%

today = datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    for category in categories_content:
        printlog(f"The category is {category}")
        main(category, today)
    printlog(f"This is the end of all the posts on {today}")

