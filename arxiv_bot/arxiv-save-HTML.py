#%% https://chatgpt.com/share/c8e08b83-0d2d-4430-a447-e0e14a945d8b
import requests
import os
from arxiv_function import arxiv_search, categories_content
from printlog import printlog
import argparse
# from typing import Optional

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
