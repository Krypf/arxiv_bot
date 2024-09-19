#%%
import os
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
    folder = 'arxiv_bot_keys/bluesky-passwords'
    directory_path = os.path.join(home_directory, folder)
    file_path = os.path.join(directory_path, category)

    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    return text

#%% constants
from atproto import Client
def login_bsky(category: str):
    # password
    p = read_password(category)
    # login
    client = Client(base_url='https://bsky.social')
    client.login(login='krxiv-' + category + '.bsky.social',password=p)

    # set a image 
    with open('img/ArXiv_logo_2022.png', 'rb') as f:
        img = f.read()
    thumb = client.upload_blob(img)
    return client, thumb
#%%
def test():
    print(login_bsky('gr-qc'))

if __name__ == '__main__':
    test()
