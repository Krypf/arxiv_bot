#%%
# https://chatgpt.com/share/2e11c4e2-96d3-4c1c-82a0-cbed39d6ec9a
import os
from atproto import Client, models, client_utils
from bluesky_function import read_password, read_text_file
import time
from printlog import printlog
from arxiv_function import categories_content

#%% constants
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
def shorten_authors(authors):
    authors_list = authors.split(", ")
    return authors_list[0] + " " + "et al."

def shorten_paper_info(paper_info):
    title_line, authors_line, arxiv_url, pdf_url = paper_info.split("\n")    
    authors_line = shorten_authors(authors_line)
    
    return f"{title_line}\n{authors_line}\n{arxiv_url}\n{pdf_url}"# there is not \n in the last
#%%
def main(category, date, sleep_time=1):
    client, thumb = bsky_login(category)
    text = read_text_file(category, date, parent_folder=os.path.expanduser("~/arxiv_bot"))
    # Split the text using "----" as the delimiter
    text_array = text.split("\n----\n")
    for t in text_array:
        send_post_to_bluesky(client, t, thumb)
        time.sleep(sleep_time)    
    return 0
#%%

date = '2024-08-09'

if __name__ == '__main__':
    for category in categories_content:
        printlog(f"The category is {category}")
        main(category, date)

#%% manual
# category = 'gr-qc'
# date = '2024-08-09'
# text = read_text_file(category, date, parent_folder=os.path.expanduser("~/arxiv_bot"))
# text_array = text.split("\n----\n")
# client, thumb = bsky_login(category)
# t = text_array[-1]
# send_post_to_bluesky(client, t, thumb)

# %%
