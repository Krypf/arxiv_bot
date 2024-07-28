#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
from atproto import Client
import os
#%%

def read_text_from_file(filename):
    """
    Reads and returns the text from a specified file in the home directory.

    Args:
        filename: The name of the file to read from.

    Returns:
        The content of the file as a string.
    """
    # Get the path to the home directory
    home_directory = os.path.expanduser("~")

    # Construct the full file path
    directory_path = os.path.join(home_directory, 'bluesky-passwords')
    file_path = os.path.join(directory_path, filename)

    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    return text

#%%
def main(category, text):
    # password
    content = read_text_from_file(category)
    
    client = Client(base_url='https://bsky.social')

    client.login(login='krxiv-' + category + '.bsky.social',password=content)

    client.send_post(text)

    return 0

category = 'gr-qc'
text = 'Hello, Bluesky?'
main(category, text)

