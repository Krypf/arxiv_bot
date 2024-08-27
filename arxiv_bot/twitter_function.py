#%%
import os

def load_credentials(category):
    """
    Reads and returns the text from keys in the directory.
    Args:
        category: The name of the file to read from.
    Returns:
        The dictionaries of the file as a string.
    """
    # Get the path to the home directory
    home_directory = os.path.expanduser("~")
    # Construct the full file path
    folder = 'twitter-keys'
    directory_path = os.path.join(home_directory, folder)
    file_path = os.path.join(directory_path, category)

    credentials = {}
    # Read the content of the file
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by the first occurrence of ':'
                key, value = line.strip().split(': ', 1)
                credentials[key] = value
        return credentials
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#%%
import tweepy

def twitter_login(category):
    # Load the credentials into a dictionary
    credentials_dict = load_credentials(category)

    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=credentials_dict['API Key'],
        consumer_secret=credentials_dict['API Key Secret'],
        access_token=credentials_dict['Access Token'],
        access_token_secret=credentials_dict['Access Token Secret']
    )
    return client

# Function to read content from a text file and tweet it

from printlog import printlog
from bluesky_function import shorten_paper_info

def make_a_tweet(title_line, authors_line, arxiv_url):
    tw = str()
    tw += (title_line + '\n')
    tw += (arxiv_url)# only an object arxiv_url
    tw += ('\n' + authors_line)
    return tw

def send_post_to_twitter(client, text, thumb=None, max_letter=280):
    t = text
    if len(t) == 0:
        # last entry
        t = 'These are all new submissions for today.'
        client.create_tweet(text=t)
        printlog(f"posted\n{t}")
        return None
    if len(t) > max_letter:
        t = shorten_paper_info(t)
        printlog(f"Tweet content exceeds {max_letter} characters. The shorten_paper_info shortened the text.")

    try:
        # Check if the tweet content is within Twitter's character limit
        # Post Tweet
        title_line, authors_line, arxiv_url, pdf_url = t.split("\n") 
        tw = make_a_tweet(title_line, authors_line, arxiv_url)
        client.create_tweet(text=tw)
        print("Tweet posted successfully!")
        printlog(f"posted\n{t}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")

    except tweepy.errors.TweepyException as e:
        print(f"Error occurred: {e}")

    # tb = make_a_rich_text(title_line, authors_line, arxiv_url)
    # embed_external = make_a_linkcard(title_line, pdf_url, thumb)
    

    printlog(f"posted\n{t}")

    return None

if __name__ == '__main__':
    # Specify the file you want to read from
    category = credentials_file = "gr-qc"

    # Load the credentials into a dictionary
    credentials_dict = load_credentials(credentials_file)

    # Print the dictionary
    if credentials_dict:
        print(credentials_dict)
        print(credentials_dict['API Key'])


# %%
