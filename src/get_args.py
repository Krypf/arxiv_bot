#%%
from argparse import ArgumentParser
from datetime import datetime

def html_args():
    parser = ArgumentParser(description="Generate arXiv list URL.")
    # parser.add_argument("--category", required=True, help="The category for the arXiv submissions (e.g., gr-qc).")
    parser.add_argument("--submissions", default="new", help="The type of submissions (e.g., new, recent).")
    parser.add_argument("--skip", default="", help="Number of submissions to skip.")
    parser.add_argument("--show", default="", help="Number of submissions to show.")
    args = parser.parse_args()
    return args

def date_args():
    parser = ArgumentParser(description='Process some dates.')
    parser.add_argument('--date', type=str, help='The (current) date')
    return parser.parse_args()

def get_today():
    args = date_args()
    if args.date:
        today = args.date
    else:
        today = datetime.now().strftime('%Y-%m-%d')
    return today
#%% https://chatgpt.com/share/7dfbd5e5-9c8d-4939-a815-efd595b5f229
from typing import List
def read_inner_file(file = '', folder='', extension = '.txt') -> List[str]:
    
    file_name = file + extension
    
    if folder != '':
        file_name = folder + '/' + file_name
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            # read each line
            lines = file.readlines()
            # Strip newline characters from each line
            categories_list = [line.strip() for line in lines]
            return categories_list
    except FileNotFoundError:
        exit(f"File '{file_name}' not found in the current directory.")
        return []
    except Exception as e:
        exit(str(e))
        return []

categories_content = read_inner_file(file='categories', folder='src')# the current directory is arxiv_bot and the subfolder is src
if __name__ == '__main__':
    print(f'categories_content is {categories_content}')
