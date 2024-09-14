#%%
import os
from printlog import printlog

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

def login_twitter(category):
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

from arxiv_function import ArxivPost

class Twitter(ArxivPost):
    # Function to read content from a text file and tweet it

    def make_tweet(self):
        return '\n'.join([self.title, self.pdf_url, self.authors, self.abs_url])

    def send_post_to_twitter(self, client, thumb=None, max_letter=280):
        # Check if the tweet content is within Twitter's character limit
        self = self.shorten_long_paper_info(max_letter)
        try:
            # Post Tweet
            tweet = self.make_tweet()
            client.create_tweet(text=tweet)
            printlog(f"Target article posted on Twitter: {self.title}")
        except tweepy.errors.TweepyException as e:
            printlog(f"Error occurred: {e}")
            # e.g. 429 TooManyRequests
            return e

        return None


#%%
def test():
    # Specify the file (category) you want to read from
    credentials_file = "gr-qc"

    # Load the credentials into a dictionary
    credentials_dict = load_credentials(credentials_file)

    # Print the dictionary
    if credentials_dict:
        print("Check if the API Key starts with", credentials_dict['API Key'][:3])
        for key, value in credentials_dict.items():
            print(f"{key}: {value[:3]}")

if __name__ == '__main__':
    test()


# %%
