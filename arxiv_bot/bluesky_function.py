#%%
import os
from arxiv_function import cd_arxiv_bot
from printlog import printlog

#%%

def read_password(category):
    """
    Reads and returns the text from a password in the directory.

    Args:
        category: The name of the file to read from.

    Returns:
        The content of the file as a string.
    """
    # Get the path to the home directory
    home_directory = os.path.expanduser("~")

    # Construct the full file path
    folder = 'bluesky-passwords'
    directory_path = os.path.join(home_directory, folder)
    file_path = os.path.join(directory_path, category)

    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    return text

def read_text_file(category, date, parent_folder=str()):
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
