#%%
from arxiv_function import ArxivText, ArxivSoup, categories_content, get_today

def sub(obj: ArxivText):     
    soup = ArxivSoup(obj.read_HTML_soup('new'))
    number_new_submissions = (soup).cross_list_number()
    iterator = map(str, range(1, number_new_submissions))# start with 1
    obj.save_all_in(iterator, soup)    
    return None

def main():
    today = get_today()
    for category in categories_content:
        obj = ArxivText(category, today, extension='.json')
        sub(obj)
    return 0

if __name__ == '__main__':
    main()
