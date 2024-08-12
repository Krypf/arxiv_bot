#%%
import arxiv
from datetime import datetime
import os
from typing import List
from printlog import printlog

#%%
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

#%% https://chatgpt.com/share/7dfbd5e5-9c8d-4939-a815-efd595b5f229
def read_categories_file(folder='') -> List[str]:
    cd_arxiv_bot()
    
    file_name = 'categories.txt'
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
#%% constants

categories_content = read_categories_file('arxiv_bot')# the current directory is arxiv_bot and the subfolder is arxiv_bot

if __name__ == '__main__':
    print('This is a module arxiv_function.py')
    print(f'categories_content is {categories_content}')
