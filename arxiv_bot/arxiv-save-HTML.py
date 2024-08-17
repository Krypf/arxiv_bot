#%% https://chatgpt.com/share/c8e08b83-0d2d-4430-a447-e0e14a945d8b
import requests
import os
from arxiv_function import categories_content
from printlog import printlog
import argparse
# from typing import Optional
#%% https://chatgpt.com/share/c59404fb-255c-42db-892a-c19c00d92e8c
class arxiv_search:
    def __init__(self, category: str, submissions: str = "new", skip: str = "", show: str = ""):
        self.category = category
        self.submissions = submissions
        self.skip = skip
        self.show = show

    def make_url(self):
        # Construct the URL based on the attributes
        url = f"https://arxiv.org/list/{self.category}/{self.submissions}"
        
        # Add query parameters if skip or show are provided
        if self.skip or self.show:
            url += "?"
        if self.skip:
            url += f"skip={self.skip}"
            if self.show:
                url += "&"
        if self.show:
            url += f"show={self.show}"
        
        return url

#%%

def main(obj: arxiv_search):
    # Directory to save the file
    directory = "HTML"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # URL to fetch
    url = obj.make_url()
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # File path to save the HTML content
        file_path = os.path.join(directory, "arxiv_" + obj.category + "_" + obj.submissions + ".html")
        
        # Save the HTML content to a file
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(response.text)
        printlog(f"HTML source has been saved to {file_path}")
    else:
        printlog(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return 0
#%%
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate arXiv list URL.")

    # parser.add_argument("--category", required=True, help="The category for the arXiv submissions (e.g., gr-qc).")
    parser.add_argument("--submissions", default="new", help="The type of submissions (e.g., new, recent).")
    parser.add_argument("--skip", default="", help="Number of submissions to skip.")
    parser.add_argument("--show", default="", help="Number of submissions to show.")

    args = parser.parse_args()

    for category in categories_content:
        obj = arxiv_search(category, args.submissions, args.skip, args.show)
        main(obj)
