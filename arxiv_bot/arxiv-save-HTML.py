#%% https://chatgpt.com/share/c8e08b83-0d2d-4430-a447-e0e14a945d8b
import os
import sys
import argparse
from arxiv_function import ArxivSearch, categories_content
from printlog import printlog
# from typing import Optional

#%%
def sub(obj: ArxivSearch):
    response = obj.get_html()
    if response.status_code == 200:
        # Save the HTML content to a file
        with open(obj.file_path, "w", encoding='utf-8') as file:
            file.write(response.text)
        printlog(f"HTML source has been saved to {obj.file_name}")
    else:
        printlog(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        sys.exit(1)  # Exit the program

    return None

def main():
    # Directory to save the file
    directory = "HTML"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    parser = argparse.ArgumentParser(description="Generate arXiv list URL.")
    # parser.add_argument("--category", required=True, help="The category for the arXiv submissions (e.g., gr-qc).")
    parser.add_argument("--submissions", default="new", help="The type of submissions (e.g., new, recent).")
    parser.add_argument("--skip", default="", help="Number of submissions to skip.")
    parser.add_argument("--show", default="", help="Number of submissions to show.")
    
    args = parser.parse_args()
    for category in categories_content:
        obj = ArxivSearch(category, args.submissions, args.skip, args.show)
        sub(obj)
    return 0

#%%
if __name__ == "__main__":
    main()
