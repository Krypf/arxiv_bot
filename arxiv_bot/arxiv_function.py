#%%
import arxiv
from datetime import datetime
import os
from typing import List
from printlog import printlog
from bs4 import BeautifulSoup

#%% https://chatgpt.com/share/c59404fb-255c-42db-892a-c19c00d92e8c
class ArxivSearch:
    def __init__(self, category: str, submissions: str = "new", skip: str = "", show: str = ""):
        self.category = category
        self.submissions = submissions
        self.skip = skip
        self.show = show

    def make_url(self):
        # Construct the URL based on the attributes
        url = f"https://arxiv.org/list/{self.category}/{self.submissions}"
        
        # Add query parameters if skip or show are provided
        if self.skip or self.show:
            url += "?"
        if self.skip:
            url += f"skip={self.skip}"
            if self.show:
                url += "&"
        if self.show:
            url += f"show={self.show}"
        
        return url

#%%
def cd_arxiv_bot():
    # Get the current working directory
    current_directory = os.getcwd()

    # Define the target directory path
    folder_strings = '~/arxiv_bot'
    target_directory = os.path.expanduser(folder_strings)

    # Change to the target directory if not already there
    if current_directory != target_directory:
        os.chdir(target_directory)
        printlog(f"Changed directory to {folder_strings}")
    else:
        printlog(f"Already in {folder_strings}")
        
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

#%%
def read_text_file(category: str, date: str, parent_folder=str()):
    # Define the path to the file
    file_name = category + '-' + date + '.txt'
    file_path = os.path.join(parent_folder, category, file_name)
    # print(file_path)
    # Check if the file exists
    if not os.path.exists(file_path):
        printlog(f"File {file_name} does not exist in the specified directory.")
        cd_arxiv_bot()

    # Open and read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content

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

#%% https://chatgpt.com/share/7dfbd5e5-9c8d-4939-a815-efd595b5f229
def read_inner_file(file = '', folder='') -> List[str]:
    cd_arxiv_bot()
    
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

def read_HTML(category, submissions="new"):
    # Specify the file path to the HTML content located in the HTML folder
    directory = "HTML"
    file_path = os.path.join(directory, "arxiv_" + category + "_" + submissions + ".html")
    # Read the HTML content from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def arxiv_formatted_date(date_str):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Format the date as "Fri, 16 Aug 2024"
    formatted_date = date_obj.strftime('%a, %d %b %Y')

    return (formatted_date)

#%%
def post_last(t, today):
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
    
    return f"{title_line}\n{authors_line}\n{arxiv_url}\n{pdf_url}"# there is not \n in the last


#%%
# no usage
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
