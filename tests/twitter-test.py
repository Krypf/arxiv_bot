#%%
file_name = 'tests/import_module.py'
with open(file_name, 'r') as file:
    script = file.read()
exec(script)
#%%
# Now you can import the module
# import arxiv_function
from twitter_function import load_credentials
from arxiv_function import categories_content

import tweepy
import os
# Specify the file you want to read from
category = credentials_file = categories_content[0]

# Load the credentials into a dictionary
credentials_dict = load_credentials(credentials_file)

# Authenticate to Twitter
client = tweepy.Client(
    consumer_key=credentials_dict['API Key'],
    consumer_secret=credentials_dict['API Key Secret'],
    access_token=credentials_dict['Access Token'],
    access_token_secret=credentials_dict['Access Token Secret']
)

# Create API object
# api = tweepy.API(auth)
# print(api)
# Function to read content from a text file and tweet it
def tweet_from_file(file_name):
    parent_folder = 'tests'
    file_path = os.path.join(parent_folder, file_name)
    try:
        with open(file_path, 'r') as file:
            tweet_content = file.read().strip()
            print(tweet_content)
            # Check if the tweet content is within Twitter's character limit
            if len(tweet_content) <= 280:
                # Post Tweet
                client.create_tweet(text=tweet_content)
                print("Tweet posted successfully!")
            else:
                print("Tweet content exceeds 280 characters. Please shorten the text.")
                
    except FileNotFoundError:
        print(f"File {file_path} not found.")

    except tweepy.errors.TweepyException as e:
        print(file_path)
        print(f"Error occurred: {e}")

# Specify the file you want to tweet from
tweet_file = "tweet.txt"
tweet_from_file(tweet_file)

# %%
