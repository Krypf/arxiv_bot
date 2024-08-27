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
#%% constants
from atproto import Client, client_utils, models

def bsky_login(category):
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
def make_a_rich_text(title_line, authors_line, arxiv_url):
    tb = client_utils.TextBuilder()
    tb.text(title_line + '\n')
    tb.link(arxiv_url, arxiv_url)
    tb.text('\n' + authors_line)
    return tb

def make_a_linkcard(title_line, pdf_url, thumb):
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
def shorten_authors(authors):
    authors_list = authors.split(", ")
    return authors_list[0] + " " + "et al."

# 無駄が多いので後で shorten_paper_info を修正したい

def shorten_paper_info(paper_info):
    title_line, authors_line, arxiv_url, pdf_url = paper_info.split("\n")    
    authors_line = shorten_authors(authors_line)
    
    return f"{title_line}\n{authors_line}\n{arxiv_url}\n{pdf_url}"# there is not \n in the last

def send_post_to_bluesky(client, text, thumb, max_letter=300):
    t = text
    if len(t) == 0:
        # last entry
        t = 'These are all new submissions for today.'
        client.send_post(t)
        printlog(f"posted\n{t}")
        return None
    if len(t) > max_letter:
        t = shorten_paper_info(t)
    
    title_line, authors_line, arxiv_url, pdf_url = t.split("\n") 
    tb = make_a_rich_text(title_line, authors_line, arxiv_url)
    embed_external = make_a_linkcard(title_line, pdf_url, thumb)
    
    client.send_post(tb, embed=embed_external)
    printlog(f"posted\n{t}")

    return None

#%%
