#%%
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime

from arxiv_function import save_text_append, categories_content

def read_HTML(category):
    # Specify the file path to the HTML content located in the HTML folder
    directory = "HTML"
    file_path = os.path.join(directory, "arxiv_" + category + "_new.html")
    # Read the HTML content from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

#%% https://chatgpt.com/share/1b7cf3d0-66c0-43f2-a651-3c5cec21d345
def cross_list_number(soup) -> str:
    cross_list_item = soup.find('a', string="Cross-lists")
    # print(cross_list_item)
    if cross_list_item:
        href = cross_list_item.get('href')
        number = re.search(r'\d+', href).group()
        # print(f'Extracted number: {number}')
    return (number)
#%% https://chatgpt.com/share/bc424881-9f53-49ed-9ed9-c145764ba7ab
def find_dt_and_dd(soup, item_number: str):
    num = item_number
    # Find the <a> element with name='item' + num
    a_element = soup.find('a', attrs={'name': 'item' + (item_number)})

    if a_element:
        # Get the parent <dt> element
        dt_element = a_element.find_parent('dt')
        if dt_element:
            # Find the next <dd> sibling element
            dd_element = dt_element.find_next_sibling('dd')
            if dd_element:
                # print(f"<dt>: {dt_element}")
                # print(f"<dd>: {dd_element}")
                return dt_element, dd_element
            else:
                print(f"No <dd> found after <dt> containing <a name='item{num}'>[{num}]</a>")
        else:
            print(f"No <dt> found containing <a name='item{num}'>[{num}]</a>")
    else:
        print(f"No <a name='item{num}'>[{num}]</a> found")

    return 0
    
#%%
def get_arxiv_link(soup_dt):
    # Find the <a> tag with title "Abstract"
    abstract_link = soup_dt.find('a', title='Abstract')

    # Extract the href attribute
    arxiv_link = abstract_link['href'] if abstract_link else None

    # Construct the full URL
    if arxiv_link:
        arxiv_url = f"https://arxiv.org{arxiv_link}"
    else:
        arxiv_url = None
        
    return arxiv_url

def get_title_and_authors(soup_dd):
    # Extract the title
    title_div = soup_dd.find('div', class_='list-title')
    title = title_div.get_text(strip=True).split(':', 1)[-1].strip() if title_div else None

    # Extract the authors
    authors_div = soup_dd.find('div', class_='list-authors')
    authors = ', '.join(a.get_text() for a in authors_div.find_all('a')) if authors_div else None

    # print("Title:", title)
    # print("Authors:", authors)
    return title, authors
#%%
def save_one_post(soup, item_number: str):
    soup_dt, soup_dd = find_dt_and_dd(soup, item_number)
    arxiv_url = get_arxiv_link(soup_dt)
    title, authors = get_title_and_authors(soup_dd)
    # Create dictionary
    article_info = {
        'arxiv_url': arxiv_url,
        'title': title,
        'authors': authors
    }
    text = f"Title: {article_info['title']}\n"
    text += f"Authors: {article_info['authors']}\n"
    # summary = entry.summary; text += f"Summary: {summary}\n";
    text += f"Link: {article_info['arxiv_url']}\n"
    text += "----\n"
    return text

def main(category):
    sub_folder = category
    # Create the subfolder if it does not exist
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    # make a file
    today = datetime.now().strftime('%Y-%m-%d')
    file_name = category + '-' + today + '.txt'
    # Create the file path
    file_path = os.path.join(sub_folder, file_name)
    # Create an empty file
    open(file_path, 'w').close()
    
    soup = read_HTML(category)
    number_new_submissions = cross_list_number(soup)
    # start with 1
    for i in range(1, int(number_new_submissions)):
        item_number = str(i)
        text = save_one_post(soup, item_number)
        save_text_append(text, file_path)
        
    # Display the result
    print(f"{file_name} has been saved.")
    return 0

category = categories_content[0]
main(category)

#%% error 
def check_no_entry():
    if not True:
        save_text_append("No entries found for today.", file_path)
