#%%
file_name = 'tests/import_module.py'
with open(file_name, 'r') as file:
    script = file.read()
exec(script)
# Now you can import the original module
#%%
import os
from arxiv_function import read_categories_file

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

categories_content = read_categories_file(folder='arxiv_bot')
for category in categories_content:
    create_folder_if_not_exists(category)
