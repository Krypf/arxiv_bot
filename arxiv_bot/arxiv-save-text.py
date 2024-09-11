#%%
from datetime import datetime
from printlog import printlog
from arxiv_function import ArxivText, save_text_append, categories_content, cross_list_number, save_one_post

def sub(obj: ArxivText):
    # Create an empty file
    open(obj.file_path, 'w').close()
    
    soup = obj.read_HTML_soup(submissions='new')
    number_new_submissions = cross_list_number(soup)
    # start with 1
    for i in range(1, int(number_new_submissions)):
        item_number = str(i)
        text = save_one_post(soup, item_number)
        save_text_append(text, obj.file_path)
        
    # Display the result
    printlog(f"{obj.file_name} has been saved.")
    return 0

def main(today, categories_content=categories_content):
    for category in categories_content:
        obj = ArxivText(category, today)
        sub(obj)
    return 0

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    main(today)

