#%%
import arxiv
from datetime import datetime
import os
#%%
def get_results(category):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query="cat:" + category,
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)
    return results

#%%
def save_text_append(text, file_path):
    """
    Appends the specified text to the given file.

    Args:
        text: The text to append.
        file_path: The path of the file to append to.
    """
    # Append the text to the file
    with open(file_path, 'a') as f:
        f.write(text)
#%%
def fetch_arxiv(category, date):
    sub_folder = category
    
    # Create the subfolder if it does not exist
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    
    results = get_results(category)
    # Filter entries matching today's date
    todays_entries = [result for result in results if result.updated.date() == datetime.strptime(date, '%Y-%m-%d').date()]
    
    file_name = category + '-' + date + '.txt'
    # Create the file path
    file_path = os.path.join(sub_folder, file_name)
    # Create an empty file
    open(file_path, 'w').close()

    # Display the result
    if not todays_entries:
        save_text_append("No entries found for today.", file_path)
    else:
        for entry in todays_entries:
            title = entry.title
            authors = ", ".join(author.name for author in entry.authors)
            summary = entry.summary
            link = entry.entry_id
            
            text = f"Title: {title}\n"
            text += f"Authors: {authors}\n"
            text += f"Summary: {summary}\n"
            text += f"Link: {link}\n"
            text += "----\n"
            save_text_append(text, file_path)

if __name__ == '__main__':
    print('This is a module arxiv_function.py')
