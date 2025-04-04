#%%
from src.utils.get_args import get_args, get_today
from src.utils.printlog import printlog
#%%
from src.save_html_json import save_html_json
from src.post_bluesky import post_bluesky
from src.post_twitter import post_twitter

def check_args():
    # Ask for user confirmation with y/n input
    while True:
        user_input = input("Do you want to continue? (y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            if user_input == 'y':
                print("You chose yes.")
                pass
            else:
                print("You chose no.")
                exit('1')
            break
        else:
            print("Please enter 'y' or 'n'.")
            exit('2')


def sub(num = 7, twi = 5):
    args = get_args()
    today = get_today(args)
    print(args)
    print(num, twi)
    check_args()
    # save_html_json(today, args, _check=True)
    # post_bluesky(today, num = num)
    post_twitter(today, twi = twi)
    printlog(f"This is the end of all the posts on {today} (sub.py).")
    return 0

if __name__ == '__main__':
    sub(twi = 4)