#%%
import requests
import os
import arxiv_function
#%% constants
categories_content = arxiv_function.read_categories_file('arxiv_bot')# the current directory is arxiv_bot and the subfolder is arxiv_bot
# Directory to save the file
directory = "HTML"
#%%
def main(category):
    # URL to fetch
    url = "https://arxiv.org/list/" + category + "/new"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # File path to save the HTML content
        file_path = os.path.join(directory, "arxiv_" + category + "_new.html")
        
        # Save the HTML content to a file
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML source has been saved to {file_path}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return 0
#%%

for category in categories_content:
    main(category)
