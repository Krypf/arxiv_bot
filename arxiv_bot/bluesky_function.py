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
from arxiv_function import ArxivPost

class Bluesky(ArxivPost):
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
        printlog(f"Target article posted on Bluesky: {self.title}")

        return None

#%%
