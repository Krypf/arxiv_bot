#%%
import os
from src.utils.get_args import read_inner_file

def create_folder_if_not_exists(folder_name):
    """
    Create a folder with the given name in the current directory if it does not already exist.

    :param folder_name: Name of the folder to be created
    """
    # Create the folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f'Folder "{folder_name}" has been created.')
    else:
        print(f'Folder "{folder_name}" already exists.')

categories_content = read_inner_file(file='categories', folder='src')
for category in categories_content:
    create_folder_if_not_exists(f"data/{category}")
