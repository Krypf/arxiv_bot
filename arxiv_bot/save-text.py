#%%
from arxiv_function import ArxivText, ArxivSoup, categories_content
from get_args import get_today

def sub(obj: ArxivText):
    # Create an empty file
    open(obj.file_path, 'w').close()
    
    soup = ArxivSoup(obj.read_HTML_soup('new'))
    number_new_submissions = soup.cross_list_number()
    iterator = map(str, range(1, number_new_submissions))# start with 1
    obj.save_all_in(iterator, soup)

    return None

def main():
    today = get_today()
    
    for category in categories_content:
        obj = ArxivText(category, today, extension = '.txt')
        sub(obj)
    return 0

if __name__ == '__main__':
    main()
