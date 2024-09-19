#%%
from arxiv_function import ArxivText
from utils.get_args import get_today, categories_content

def save_json():
    today = get_today()
    for category in categories_content:
        obj = ArxivText(category, today, extension='.json')
        obj.save_one_json()
    return 0

main = save_json
if __name__ == '__main__':
    main()
