#%%
from src.core.arxiv_function import ArxivSearch, ArxivText, ArxivSoup 
from src.utils.get_args import get_args, get_today, categories_content

def sub(obj: ArxivText):
    obj.confirm_initialize()
    
    search = ArxivSearch(obj.category, submissions = 'recent')
    soup = ArxivSoup(search.read_HTML())
    # soup = ArxivSoup(obj.read_HTML_soup('recent'))
    item_numbers = search.extract_skip_numbers(obj.date, _printlog=False)
    
    iterator = map(str, range(*item_numbers))
    obj.save_all_in(iterator, soup)
    return None

def main():
    args = get_args()
    
    date = get_today(args)
    for category in categories_content:
        # extension = '.json' not .txt
        obj = ArxivText(category, date, extension = '.json')
        sub(obj)
    return 0

if __name__ == '__main__':
    main()
    
