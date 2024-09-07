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
    folder = 'arxiv_bot_keys/twitter-keys'
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
        printlog(f"File {file_path} not found.")
        return None
    except Exception as e:
        printlog(f"An error occurred: {e}")
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


def make_tweet(title_line, authors_line, arxiv_url, pdf_url):
    tw = str()
    tw += (title_line + '\n')
    tw += (arxiv_url)# only an object arxiv_url
    tw += ('\n' + authors_line)
    tw += ('\n' + pdf_url)
    return tw

from printlog import printlog
from arxiv_function import post_last, shorten_paper_info

def send_post_to_twitter(client, text, thumb=None, max_letter=280, today='today'):
    t = text
    if len(t) == 0:
        t = post_last(t, today)
        client.create_tweet(text=t)
        return None
    if len(t) > max_letter:
        # Check if the tweet content is within Twitter's character limit
        t = shorten_paper_info(t, max_letter)
    try:
        # Post Tweet
        title_line, authors_line, arxiv_url, pdf_url = t.split("\n")
        tw = make_tweet(title_line, authors_line, arxiv_url, pdf_url)
        client.create_tweet(text=tw)
        # print("Tweet posted successfully!")
        printlog(f"posted on Twitter\n{t}")
    except tweepy.errors.TweepyException as e:
        printlog(f"Error occurred: {e}")

    return None

#%%
from arxiv_function import ArxivText

def reduce_to_api_maximum(text_array, category: str, api_maximum: int):
    m = api_maximum
    text_array = text_array[:m-2]
    t = "Twitter API v2 limits posts to 50 per day. All the posts including the remaining submissions are posted on Bluesky: " + f"https://bsky.app/profile/krxiv-{category}.bsky.social"
    text_array.append(t)
    text_array.append("")
    return text_array
    
def Twitter_with_api_max(iteration, client_twitter, text, date, api_maximum: int = 100):
    # Twitter
    # 1500 / month
    if iteration <= api_maximum - 2:
        send_post_to_twitter(client_twitter, text, today=date)
    elif iteration == api_maximum - 1:
        t = "Twitter API v2 limits posts to 50 per day. All the posts including the remaining submissions are posted on Bluesky: " + f"https://bsky.app/profile/krxiv-{category}.bsky.social"
        client_twitter.create_tweet(text=t)
        printlog(f"posted on Twitter\n{t}")
    elif iteration == api_maximum:
        t = ""
        send_post_to_twitter(client_twitter, t, today=date)
    else:
        pass
#%%

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
