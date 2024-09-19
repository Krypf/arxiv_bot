#%%
from core.arxiv_function import ArxivSearch, ArxivText, ArxivSoup 
from utils.get_args import categories_content, read_inner_file

def sub(obj: ArxivText):
    obj.confirm_initialize()
    
    search = ArxivSearch(obj.category, submissions = 'recent')
    soup = ArxivSoup(search.read_HTML())
    # soup = ArxivSoup(obj.read_HTML_soup('recent'))
    item_numbers = search.extract_skip_numbers(obj.date, _printlog=False)
    
    iterator = map(str, range(*item_numbers))
    obj.save_all_in(iterator, soup)
    return 0

def main():
    dates = read_inner_file(file='date', folder='src')
    date = dates[-1]
    for category in categories_content:
        obj = ArxivText(category, date, extension = '.txt')
        sub(obj)
    return 0

if __name__ == '__main__':
    main()
    
