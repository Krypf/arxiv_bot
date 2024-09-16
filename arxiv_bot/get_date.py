#%%
import argparse
from datetime import datetime
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some dates.')
    parser.add_argument('--date', type=str, help='The (current) date')
    return parser.parse_args()

def get_today():
    args = parse_arguments()
    if args.date:
        today = args.date
    else:
        today = datetime.now().strftime('%Y-%m-%d')
    return today
