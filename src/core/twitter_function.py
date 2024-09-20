#%%
import os
from src.core.printlog import printlog

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
        printlog(f"File {file_path.replace(home_directory, '~')} not found.")
        exit("load_credentials: 404")
    except Exception as e:
        printlog(f"Exception error: {e}")
        exit("load_credentials: Exception")

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
#%%
def test():
    # Specify the file (category) you want to read from
    from utils.get_args import categories_content
    twi = 5
    for category in categories_content[:twi]:
        # Load the credentials into a dictionary
        credentials_file = category
        credentials_dict = load_credentials(credentials_file)
        # Print the dictionary
        if credentials_dict:
            print(category, ":")
            print("Please check if the API Key starts with", credentials_dict['API Key'][:3])
            for key, value in credentials_dict.items():
                print(f"{key}: {value[:3]}")

if __name__ == '__main__':
    test()
# %%
