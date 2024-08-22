from twitter_function import load_credentials
from arxiv_function import categories_content

import tweepy
# Specify the file you want to read from
category = credentials_file = categories_content[0]

# Load the credentials into a dictionary
credentials_dict = load_credentials(credentials_file)

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    consumer_key=credentials_dict['API Key'],
    consumer_secret=credentials_dict['API Key Secret'],
    access_token=credentials_dict['Access Token'],
    access_token_secret=credentials_dict['Access Token Secret']
)

# Create API object
api = tweepy.API(auth)
print(api)
# Function to read content from a text file and tweet it
def tweet_from_file(filename):
    try:
        with open(filename, 'r') as file:
            tweet_content = file.read().strip()
            
            # Check if the tweet content is within Twitter's character limit
            if len(tweet_content) <= 280:
                api.update_status(tweet_content)
                print("Tweet posted successfully!")
            else:
                print("Tweet content exceeds 280 characters. Please shorten the text.")
                
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except tweepy.TweepError as e:
        print(f"Error occurred: {e.reason}")

# Specify the file you want to tweet from
# tweet_file = "tweet.txt"
# tweet_from_file(tweet_file)
