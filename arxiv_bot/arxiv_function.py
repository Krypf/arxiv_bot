#%%
import os
import re
import arxiv
from datetime import datetime
from typing import List
import requests
import sys

from bs4 import BeautifulSoup
from lxml import etree
from pyquery import PyQuery as pq

from arxiv_bot.printlog import printlog
#%% https://chatgpt.com/share/c59404fb-255c-42db-892a-c19c00d92e8c
class ArxivSearch:
    def __init__(self, category: str, submissions: str = "new", skip: str = "", show: str = "", parent_folder: str = os.path.expanduser("~/arxiv_bot")):
        self.category = category
        self.submissions = submissions
        self.skip = skip
        self.show = show
        # HTML data
        self.file_name = f"arxiv_{self.category}_{self.submissions}.html"
        # Specify the file path to the HTML content located in the HTML folder
        directory = "HTML"
        self.file_path = os.path.join(parent_folder, directory, self.file_name)

    def make_url(self):
        # Construct the URL based on the attributes
        url = f"https://arxiv.org/list/{self.category}/{self.submissions}"
        
        # Add query parameters if skip or show are provided
        if self.skip or self.show:
            url += "?"
        if self.skip:
            url += f"skip={self.skip}"
            # skip and show
            if self.show:
                url += "&"
        # the show option exists
        if self.show:
            url += f"show={self.show}"
        
        return url
    
    def read_HTML(self, library='BeautifulSoup', encoding='utf-8', parser='html.parser'):
        # Read the HTML content from the file
        with open(self.file_path, 'r', encoding=encoding) as file:
            html_content = file.read()
        
        if library == 'BeautifulSoup':
            # Parse the HTML content
            soup = BeautifulSoup(html_content, parser)
            return soup
        if library == 'lxml':                  
            # Convert to bytes (ensure it's UTF-8 encoded)
            html_bytes = html_content.encode(encoding)
            # Parse the HTML content using bytes
            tree = etree.HTML(html_bytes)
            return tree
        if library == 'pyquery':
            # Parse the HTML content
            document = pq(html_content.encode(encoding))
            return document
        else:
            raise ValueError(f"Unsupported library: {library}. Choose 'BeautifulSoup' or 'lxml' or 'pyquery'.")

    def find_text_from_HTML(self, tag, text):
        document = self.read_HTML(library='pyquery')
        # Find elements containing the search string
        elements = document(tag).filter(lambda i, e: text in pq(e).text())
        # Print matching elements and their text
        list_documents = [element.outer_html() for element in elements.items()]
        n = len(list_documents)
        if n == 1:
            document = pq(list_documents[0])
            return document
        else:
            raise IndexError(f"There are {n} matching elements.")        

    def extract_skip_number_from_list(html_string):
        # Parse the HTML with etree
        tree = etree.HTML(html_string)

        # Extract the href attribute of the <a> tag
        href = tree.xpath('//li/a/@href')[0]

        # Find the skip parameter value
        match = re.search(r'skip=(\d+)', href)
        if match:
            skip_value = match.group(1)
            return (skip_value)

    def extract_skip_numbers(self, date, _printlog=True):
        date_to_find = arxiv_formatted_date(date)
        document = self.find_text_from_HTML('ul', date_to_find)
        # Find <li> element containing the date
        list_item_with_date = document('li').filter(lambda index, element: date_to_find in pq(element).html())
        # Get the next <li> element after the one with the date
        if list_item_with_date:
            next_list_item = list_item_with_date.next()
            # Print the HTML of both the current <li> and the next <li>
            x = list_item_with_date.outer_html()
            X = ArxivSearch.extract_skip_number_from_list(x)
            
            y = next_list_item.outer_html()
            Y = ArxivSearch.extract_skip_number_from_list(y)
            if _printlog:
                printlog(f"List Item with Date:\n{x}")
                printlog(f"Next List Item:\n{y}")
            return (int(X) + 1, int(Y) + 1)# plus one
        else:
            printlog(f"No <li> element found with the date: {date_to_find}")
            exit('1')
    
    def get_html(self):
        # URL to fetch
        url = self.make_url()
        # Format the datetime object to the desired string format
        today = datetime.now().strftime('%A, %-d %B %Y')
        # Send a GET request to the webpage
        response = ArxivSearch.check_date_in_html(url, today)
        return response

    def check_date_in_html(url: str, date: str) -> None:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            # Check if the request was successful
            response.raise_for_status()  # Raise an error for bad responses (e.g., 404 or 500)

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, features="xml")
            
            # Check if the specified date is present in the HTML content
            if not any(date in element.text for element in soup.find_all()):
                printlog(f"Specified date ({date}) not found in HTML. No entries found for today. Exiting program.")            
                sys.exit(1)  # Exit the program
            else:
                return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            sys.exit(1)  # Exit the program in case of an error with the request

#%%

def arxiv_formatted_date(date_str):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Format the date as "Fri, 16 Aug 2024"
    formatted_date = date_obj.strftime('%a, %-d %b %Y')

    return (formatted_date)

#%%
def cd_arxiv_bot(_printlog=True):
    # Get the current working directory
    current_directory = os.getcwd()

    # Define the target directory path
    folder_strings = '~/arxiv_bot'
    target_directory = os.path.expanduser(folder_strings)

    # Change to the target directory if not already there
    if current_directory != target_directory:
        os.chdir(target_directory)
        if _printlog: printlog(f"Changed directory to {folder_strings}")
    else:
        if _printlog: printlog(f"Already in {folder_strings}")
        
#%% # https://chatgpt.com/share/a02b3fb5-fb86-4de9-a1fa-5f001dcca01f
class ArxivText:
    def __init__(self, category: str, date: str, parent_folder: str = os.path.expanduser("~/arxiv_bot")):
        self.category = category
        self.date = date
        self.parent_folder = parent_folder
        # Define the path to the file
        self.file_name = f"{self.category}-{self.date}.txt"
        self.file_path = os.path.join(self.parent_folder, self.category, self.file_name)
        
    def read_content(self):
        # Check if the file exists
        if not os.path.exists(self.file_path):
            printlog(f"File {self.file_name} does not exist in the specified directory.")
            cd_arxiv_bot()

        # Open and read the content of the file
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return content

    def read_HTML_soup(self, submissions: str):
        obj = ArxivSearch(self.category, submissions)
        return obj.read_HTML()
    
    def append_to_path(self, text):
        """
        Appends the specified text to the given file.

        Args:
            text: The text to append.
            file_path: The path of the file to append to.
        """
        # Append the text to the file
        with open(self.file_path, 'a') as f:
            f.write(text)

#%%
class ArxivSoup():
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
    
    # https://chatgpt.com/share/bc424881-9f53-49ed-9ed9-c145764ba7ab
    def find_dt_and_dd(self, item_number: str):
        num = item_number
        # Find the <a> element with name='item' + num
        a_element = self.soup.find('a', attrs={'name': 'item' + (num)})

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
                    printlog(f"No <dd> found after <dt> containing <a name='item{num}'>[{num}]</a>")
            else:
                printlog(f"No <dt> found containing <a name='item{num}'>[{num}]</a>")
        else:
            printlog(f"No <a name='item{num}'>[{num}]</a> found")

        return 0
        
    # https://chatgpt.com/share/1b7cf3d0-66c0-43f2-a651-3c5cec21d345
    def cross_list_number(self) -> int:
        cross_list_item = self.soup.find('a', string="Cross-lists")
        # print(cross_list_item)
        if cross_list_item:
            href = cross_list_item.get('href')
            number = re.search(r'\d+', href).group()
            # print(f'Extracted number: {number}')
            return int(number)
        else:
            raise ValueError("Cross-lists link not found in the provided HTML.")
    
    def get_one_post(self, item_number: str):
        soup_dt, soup_dd = self.find_dt_and_dd(item_number)# not self.soup. ...
        if "cross-list" in soup_dt.get_text():
            printlog(f"Number {item_number} included in cross-list")
            return ""
        arxiv_url, pdf_url = ArxivSoup.get_arxiv_link(soup_dt)
        title, authors = ArxivSoup.get_title_and_authors(soup_dd)
        # Create dictionary
        article_info = {
            'arxiv_url': arxiv_url,
            'pdf_url': pdf_url,
            'title': title,
            'authors': authors
        }
        text = f"{article_info['title']}\n"
        text += f"{article_info['authors']}\n"
        # summary = entry.summary; text += f"Summary: {summary}\n";
        text += f"{article_info['arxiv_url']}\n"
        text += f"{article_info['pdf_url']}\n"
        text += "----\n"
        return text
    
    def get_one_article(self, item_number: str):
        soup_dt, soup_dd = self.find_dt_and_dd(item_number)# not self.soup. ...
        if "cross-list" in soup_dt.get_text():
            printlog(f"Number {item_number} included in cross-list")
            return ""
        arxiv_url, pdf_url = ArxivSoup.get_arxiv_link(soup_dt)
        title, authors = ArxivSoup.get_title_and_authors(soup_dd)
        # Create dictionary
        name = f'item{item_number}'

        article_info = {
            'arxiv_url': arxiv_url,
            'pdf_url': pdf_url,
            'title': title,
            'authors': authors
        }
        # Dictionary with dynamic name as key
        article = {
            name: article_info
        }
        return article

    def get_arxiv_link(soup_dt):
        # Find the <a> tag with title "Abstract"
        abstract_link = soup_dt.find('a', title='Abstract')
        download_pdf_link = soup_dt.find('a', title='Download PDF')
        # Extract the href attribute
        arxiv_link = abstract_link['href'] if abstract_link else None
        pdf_link = download_pdf_link['href'] if download_pdf_link else None
        # Construct the full URL
        arxiv_url = f"https://arxiv.org{arxiv_link}" if arxiv_link else None
        pdf_url = f"https://arxiv.org{pdf_link}" if pdf_link else None
            
        return arxiv_url, pdf_url

    def get_title_and_authors(soup_dd):
        # Extract the title
        title_div = soup_dd.find('div', class_='list-title')
        title = title_div.get_text(strip=True).split(':', 1)[-1].strip() if title_div else None
        # Extract the authors
        authors_div = soup_dd.find('div', class_='list-authors')
        authors = ', '.join(a.get_text() for a in authors_div.find_all('a')) if authors_div else None
        return title, authors



#%% https://chatgpt.com/share/7dfbd5e5-9c8d-4939-a815-efd595b5f229
def read_inner_file(file = '', folder='') -> List[str]:
    cd_arxiv_bot(_printlog=False)
    
    extension = '.txt'
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
        printlog(f"File '{file_name}' not found in the current directory.")
        return []
    except Exception as e:
        printlog(str(e))
        return []

#%%
def post_last(today):
    t = f"These are all of the new submissions on {today}."
    printlog(f"posted\n{t}")
    return t

def shorten_authors(authors):
    authors_list = authors.split(", ")
    return authors_list[0] + " " + "et al."

# 無駄が多いので後で shorten_paper_info を修正したい

def shorten_paper_info(paper_info, max_letter: int):
    title_line, authors_line, arxiv_url, pdf_url = paper_info.split("\n")    
    authors_line = shorten_authors(authors_line)
    printlog(f"Tweet content exceeds {max_letter} characters. The shorten_paper_info shortened the text.")
    
    _ans = f"{title_line}\n{authors_line}\n{arxiv_url}\n{pdf_url}"
    if len(_ans) <= max_letter: 
        return _ans # there is not \n in the last
    else:
        exit('shorten_paper_info: 1')


#%%
# no usage

#%%
def save_text_append(text, file_path):
    """
    Appends the specified text to the given file.

    Args:
        text: The text to append.
        file_path: The path of the file to append to.
    """
    # Append the text to the file
    with open(file_path, 'a') as f:
        f.write(text)

def my_replace(text: str) -> str:
    text = text.replace('Title:\n          ', 'Title: ')
    text = text.replace('\n        ', '\n')
    return text

def get_results(category, _max_results=100):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query="cat:" + category,
        max_results=_max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)
    return results

#%%
def fetch_arxiv(category, date, __max_results=100):
    sub_folder = category
    
    # Create the subfolder if it does not exist
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    
    results = get_results(category, _max_results = __max_results)
    # Filter entries matching today's date
    todays_entries = [result for result in results if result.updated.date() == datetime.strptime(date, '%Y-%m-%d').date()]
    
    file_name = category + '-' + date + '.txt'
    # Create the file path
    file_path = os.path.join(sub_folder, file_name)
    # Create an empty file
    open(file_path, 'w').close()

    # Display the result
    if not todays_entries:
        save_text_append("No entries found for today.", file_path)
    else:
        for entry in todays_entries:
            title = entry.title
            authors = ", ".join(author.name for author in entry.authors)
            
            link = entry.entry_id
            
            text = f"Title: {title}\n"
            text += f"Authors: {authors}\n"
            # summary = entry.summary; text += f"Summary: {summary}\n";
            text += f"Link: {link}\n"
            text += "----\n"
            save_text_append(text, file_path)
    printlog(f"{file_name} has been saved.")

#%% constants

categories_content = read_inner_file(file='categories', folder='arxiv_bot')# the current directory is arxiv_bot and the subfolder is arxiv_bot

if __name__ == '__main__':
    print('This is a module arxiv_function.py')
    print(f'categories_content is {categories_content}')
