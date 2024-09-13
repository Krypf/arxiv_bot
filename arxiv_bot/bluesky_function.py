#%%
import os
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
    folder = 'arxiv_bot_keys/bluesky-passwords'
    directory_path = os.path.join(home_directory, folder)
    file_path = os.path.join(directory_path, category)

    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    return text

#%% constants
from atproto import Client, client_utils, models

def login_bsky(category):
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
def make_rich_text(title_line, authors_line, abs_url):
    tb = client_utils.TextBuilder()
    tb.text(title_line + '\n')
    tb.link(abs_url, abs_url)
    tb.text('\n' + authors_line)
    return tb

def make_linkcard(title_line, pdf_url, thumb):
    embed_external = models.AppBskyEmbedExternal.Main(
        external = models.AppBskyEmbedExternal.External(
            title = title_line,
            description = "arXiv PDF link",
            uri = pdf_url,
            thumb=thumb.blob
        )
    )
    return embed_external
#%%

from arxiv_function import post_last, shorten_paper_info

def send_post_to_bluesky(client, text, thumb, max_letter=300, today='today'):
    t = text
    if len(t) == 0:
        t = post_last(today)
        client.send_post(t)
        return None
    if len(t) > max_letter:
        t = shorten_paper_info(t, max_letter)
    
    title_line, authors_line, abs_url, pdf_url = t.split("\n") 
    tb = make_rich_text(title_line, authors_line, abs_url)
    embed_external = make_linkcard(title_line, pdf_url, thumb)
    
    client.send_post(tb, embed=embed_external)
    printlog("Text posted on Bluesky")

    return None

#%%
