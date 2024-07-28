#%%
import arxiv
from datetime import datetime
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
def save_text_append(text, filename):
    """
    Appends the specified text to the given file.

    Args:
        text: The text to append.
        filename: The name of the file to append to.
    """
    # Append the text to the file
    with open(filename, 'a') as f:
        f.write(text)
#%%
def fetch_arxiv(category, date):
    results = get_results(category)
    # Filter entries matching today's date
    todays_entries = [result for result in results if result.updated.date() == datetime.strptime(date, '%Y-%m-%d').date()]
    
    # Create an empty file
    filename = category + '-' + date + '.txt'
    open(filename, 'w').close()

    # Display the result
    if not todays_entries:
        save_text_append("No entries found for today.", filename)
    else:
        for entry in todays_entries:
            title = entry.title
            authors = ", ".join(author.name for author in entry.authors)
            summary = entry.summary
            link = entry.entry_id
            
            print(f"Title: {title}")
            print(f"Authors: {authors}")
            print(f"Summary: {summary}")
            print(f"Link: {link}")
            print("----")
