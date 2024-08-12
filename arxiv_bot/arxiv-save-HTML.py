#%% https://chatgpt.com/share/c8e08b83-0d2d-4430-a447-e0e14a945d8b
import requests
import os
from arxiv_function import categories_content
from printlog import printlog

#%%
# Directory to save the file
directory = "HTML"
#%%
def main(category):
    # URL to fetch
    # new submissions
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
        printlog(f"HTML source has been saved to {file_path}")
    else:
        printlog(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return 0
#%%
for category in categories_content:
    main(category)
