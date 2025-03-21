#%%
from src.utils.get_args import get_args, get_today
from src.utils.printlog import printlog
#%%
from src.save_html_json import save_html_json
from src.post_bluesky import post_bluesky
from src.post_twitter import post_twitter

def sub():
    args = get_args()
    today = get_today(args)
    save_html_json(today, args, _check=True)
    post_bluesky(today)
    post_twitter(today, twi = 5)
    printlog(f"This is the end of all the posts on {today}")
    return 0

if __name__ == '__main__':
    sub()