#%%
import os
import re
from datetime import datetime
import requests
import sys
import json

from bs4 import BeautifulSoup
from lxml import etree
from pyquery import PyQuery as pq

from core.printlog import printlog
#%%
def arxiv_formatted_date(date_str):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Format the date as "Fri, 16 Aug 2024"
    formatted_date = date_obj.strftime('%a, %-d %b %Y')

    return (formatted_date)
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
        directory = "data/HTML"
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

    def extract_skip_numbers(self, date: str, _printlog=True):
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
    
    def save_one_html(self):
        # https://chatgpt.com/share/c8e08b83-0d2d-4430-a447-e0e14a945d8b
        response = self.get_html()
        if response.status_code == 200:
            # Save the HTML content to a file
            with open(self.file_path, "w", encoding='utf-8') as file:
                file.write(response.text)
            printlog(f"{self.file_name} has been saved.")
        else:
            printlog(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            sys.exit(1)  # Exit the program

        return None

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
    
    def get_one_article(self, item_number: str):
        soup_dt, soup_dd = self.find_dt_and_dd(item_number)# not self.soup. ...
        if "cross-list" in soup_dt.get_text():
            printlog(f"Number {item_number} included in cross-list")
            return ""
        abs_url, pdf_url = ArxivSoup.get_arxiv_link(soup_dt)
        title, authors = ArxivSoup.get_title_and_authors(soup_dd)
        # Create dictionary
        name = f'item{item_number}'

        article_info = {
            'name': name,
            'abs_url': abs_url,
            'pdf_url': pdf_url,
            'title': title,
            'authors': authors
        }
        return article_info
        # Dictionary with dynamic name as key
        # article = {
            # name: article_info
        # }
        # return article

    def get_one_article_text(self, item_number: str):
        # Create dictionary
        article_info = self.get_one_article(item_number)
        text = f"{article_info['title']}\n"
        text += f"{article_info['authors']}\n"
        text += f"{article_info['abs_url']}\n"
        text += f"{article_info['pdf_url']}\n"
        text += "----\n"
        return text
    
    def get_arxiv_link(soup_dt):
        # Find the <a> tag with title "Abstract"
        abstract_link = soup_dt.find('a', title='Abstract')
        download_pdf_link = soup_dt.find('a', title='Download PDF')
        # Extract the href attribute
        arxiv_link = abstract_link['href'] if abstract_link else None
        pdf_link = download_pdf_link['href'] if download_pdf_link else None
        # Construct the full URL
        abs_url = f"https://arxiv.org{arxiv_link}" if arxiv_link else None
        pdf_url = f"https://arxiv.org{pdf_link}" if pdf_link else None
            
        return abs_url, pdf_url

    def get_title_and_authors(soup_dd):
        # Extract the title
        title_div = soup_dd.find('div', class_='list-title')
        title = title_div.get_text(strip=True).split(':', 1)[-1].strip() if title_div else None
        # Extract the authors
        authors_div = soup_dd.find('div', class_='list-authors')
        authors = ', '.join(a.get_text() for a in authors_div.find_all('a')) if authors_div else None
        return title, authors

#%% # https://chatgpt.com/share/a02b3fb5-fb86-4de9-a1fa-5f001dcca01f

from core.twitter_function import login_twitter
from core.bluesky_function import login_bsky
import time

class ArxivText:
    def __init__(self, category: str, date: str, parent_folder: str = os.path.expanduser("~/arxiv_bot"), extension: str = '.txt'):
        self.category = category
        self.date = date
        self.parent_folder = parent_folder
        self.extension = extension
        self.file_name = f"{self.category}-{self.date}{self.extension}"
        # Define the path to the file
        directory = f"data/{self.category}"
        self.file_path = os.path.join(self.parent_folder, directory, self.file_name)
        
    def read_content(self):
        # Check if the file exists
        if not os.path.exists(self.file_path):
            printlog(f"File {self.file_name} does not exist in the specified directory.")
            cd_arxiv_bot()
        # Open and read the content of the file
        with open(self.file_path, 'r', encoding='utf-8') as file:
            if self.extension == '.txt':
                content = file.read()
            elif self.extension == '.json':
                content = json.load(file)
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

    def check_date_in_html(self, date: str) -> None:
            try:
                # Check if the specified date is present in the HTML content
                if not any(date in element.get_text() for element in self.soup.find_all(True)):
                    printlog(f"Specified date ({date}) not found in HTML. No entries found for today. Exiting program.")            
                    sys.exit(1)  # Exit the program
                else:
                    return 0
            except:
                sys.exit(1)  # Exit the program in case of an error with the request

    def last_post(self):
        d = arxiv_formatted_date(self.date)
        t = f"These are all of the new submissions in the {self.category} category on {d}."
        printlog(f"Post \"{t}\"")
        return t
    
    def update_bluesky(self, sleep_time=0.3):
        printlog(f"Start updating Bluesky with arxiv entries in the {self.category} category on {self.date}.")
        articles_list = self.read_content()
        client_bsky, thumb = login_bsky(self.category)
        for article in articles_list:
            article = ArxivPost(article)
            article.send_post_to_bluesky(client_bsky, thumb)
            time.sleep(sleep_time)
        client_bsky.send_post(self.last_post())
        return None
    
    def update_twitter(self, sleep_time=0.3, api_maximum=50):
        printlog(f"Start updating Twitter with arxiv entries in the {self.category} category on {self.date}.")
        articles_list = self.read_content()
        client_twitter = login_twitter(self.category)
        for article in articles_list:
            article = ArxivPost(article)
            twi_api = article.send_post_to_twitter(client_twitter)
            if twi_api:
                api_maximum = 50
                t = f"Twitter API v2 limits posts to 1500 per month ({api_maximum} per day). All the posts including the remaining submissions are posted on Bluesky: "
                t += f"https://bsky.app/profile/krxiv-{self.category}.bsky.social"
                printlog(f"Stop sending tweets. Please tweet manually:\n{t}")
                break
            time.sleep(sleep_time)
        client_twitter.create_tweet(text=self.last_post())
        return None

    def confirm_initialize(self):
        # Print current date and time to stdout
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Current date and time: {current_date}")
        print(f"The date you select is {self.date}")
        print(f"The category you select is {self.category}")

        # Ask for user confirmation with y/n input
        while True:
            user_input = input("Do you want to continue? (y/n): ").strip().lower()
            if user_input in ['y', 'n']:
                if user_input == 'y':
                    print("You chose yes.")
                else:
                    print("You chose no.")
                break
            else:
                print("Please enter 'y' or 'n'.")

        # Create an empty file
        open(self.file_path, 'w').close()
        # Open the file in write mode
        with open(self.file_path, 'w') as file:
            # You can write to the file here if needed
            file.write("")
            printlog(f"File {self.file_name} has been initialized.")
            # security: do not use the absolute file_path

        return None
    def save_all_in(self, iterator, soup: ArxivSoup):
        if self.extension == '.json':
            data = []
            for item_number in iterator:
                article = soup.get_one_article(item_number)
                data.append(article)
                with open(self.file_path, 'w') as file:
                    json.dump(data, file, indent=4)
        elif self.extension == '.txt':
            for item_number in iterator:
                text = soup.get_one_article_text(item_number)
                self.append_to_path(text)
        
        printlog(f"{self.file_name} has been saved.")
        return None
    def save_one_json(self):     
        soup = ArxivSoup(self.read_HTML_soup('new'))
        number_new_submissions = (soup).cross_list_number()
        iterator = map(str, range(1, number_new_submissions))# start with 1
        self.save_all_in(iterator, soup)    
        return None
#%%
import tweepy
from atproto import client_utils, models

class ArxivPost():
    def __init__(self, article: dict):
        self.name    = article['name']
        self.title   = article['title']
        self.authors = article['authors']
        self.abs_url = article['abs_url']
        self.pdf_url = article['pdf_url']
    
    def shorten_authors(authors):
        authors_list = authors.split(", ")
        return authors_list[0] + " " + "et al."

    def all_text(self):
        return'\n'.join([self.title, self.pdf_url, self.authors, self.abs_url])
        
    def shorten_long_paper_info(self, max_letter: int):
        if len(self.all_text()) > max_letter:
            self.authors = ArxivPost.shorten_authors(self.authors)
            printlog(f"The content of {self.title} exceeds {max_letter} characters. The shorten_long_paper_info shortened the text.")
            # renew all the text
            if len(self.all_text()) <= max_letter:
                return self
            else:
                exit('shorten_long_paper_info: 1')
        else:
            return self

    """
    Move methods to solve the
    ImportError: cannot import name 'ArxivPost' from partially initialized module 'arxiv_function' (most likely due to a circular import) (~/arxiv_bot/arxiv_bot/arxiv_function.py)    
    """
    # Twitter
    # Function to read content from a text file and tweet it
    def make_tweet(self):
        return self.all_text()

    def send_post_to_twitter(self, client, thumb=None, max_letter=280):
        # Check if the tweet content is within Twitter's character limit
        self = self.shorten_long_paper_info(max_letter)
        try:
            # Post Tweet
            tweet = self.make_tweet()
            client.create_tweet(text=tweet)
            printlog(f"Article posted on Twitter: {self.authors}. {self.title}")
        except tweepy.errors.TweepyException as e:
            printlog(f"Error occurred: {e}")
            # e.g. 429 TooManyRequests
            return e
        except tweepy.errors.Forbidden:
            printlog("403 Forbidden. You are not allowed to create a Tweet with duplicate content.")
            exit(403)

        return None
    # Bluesky
    def make_rich_text(self):
        tb = client_utils.TextBuilder()
        tb.text(self.title + '\n')
        tb.link(self.pdf_url, self.pdf_url)
        tb.text('\n' + self.authors)
        return tb

    def make_linkcard(self, thumb):
        embed_external = models.AppBskyEmbedExternal.Main(
            external = models.AppBskyEmbedExternal.External(
                title = self.title,
                description = "arXiv abstract link",
                uri = self.abs_url,
                thumb=thumb.blob
            )
        )
        return embed_external
    
    def send_post_to_bluesky(self, client, thumb, max_letter=300):
        self = self.shorten_long_paper_info(max_letter)
        
        tb = self.make_rich_text()
        embed_external = self.make_linkcard(thumb)
        
        client.send_post(tb, embed=embed_external)
        printlog(f"Article posted on Bluesky: {self.authors}. {self.title}")

        return None

if __name__ == '__main__':
    print('This is a module arxiv_function.py')
