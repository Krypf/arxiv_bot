#%%
import argparse
from datetime import datetime

def html_args():
    parser = argparse.ArgumentParser(description="Generate arXiv list URL.")
    # parser.add_argument("--category", required=True, help="The category for the arXiv submissions (e.g., gr-qc).")
    parser.add_argument("--submissions", default="new", help="The type of submissions (e.g., new, recent).")
    parser.add_argument("--skip", default="", help="Number of submissions to skip.")
    parser.add_argument("--show", default="", help="Number of submissions to show.")
    args = parser.parse_args()
    return args

def date_args():
    parser = argparse.ArgumentParser(description='Process some dates.')
    parser.add_argument('--date', type=str, help='The (current) date')
    return parser.parse_args()

def get_today():
    args = date_args()
    if args.date:
        today = args.date
    else:
        today = datetime.now().strftime('%Y-%m-%d')
    return today
