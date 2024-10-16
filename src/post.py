#%%
from src.utils.printlog import printlog
from src.utils.get_args import get_args, get_today

from src.post_bluesky import post_bluesky
from src.post_twitter import post_twitter

def post():
    args = get_args()
    
    today = get_today(args)
    post_bluesky(today)
    
    post_twitter(today)
    printlog(f"This is the end of all the posts on {today}")
    return 0

main = post

if __name__ == '__main__':
    main()
    
# %%
