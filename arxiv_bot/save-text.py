#%%
from datetime import datetime
from printlog import printlog
from arxiv_function import ArxivText, ArxivSoup, categories_content

def sub(obj: ArxivText):
    # Create an empty file
    open(obj.file_path, 'w').close()
    
    soup = ArxivSoup(obj.read_HTML_soup('new'))
    number_new_submissions = (soup).cross_list_number()
    iterator = map(str, range(1, number_new_submissions))# start with 1
    for item_number in iterator:
        text = soup.get_one_post(item_number)
        obj.append_to_path(text)
    
    # Display the result
    printlog(f"{obj.file_name} has been saved.")
    return None

def main(today, categories_content):
    for category in categories_content:
        obj = ArxivText(category, today)
        sub(obj)
    return 0

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    main(today, categories_content)
