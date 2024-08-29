#%%
from arxiv_function import ArxivSearch, save_text_append, categories_content, read_HTML, read_inner_file, arxiv_formatted_date

# Sample HTML
category = categories_content[0]
dates = read_inner_file(file='date', folder='arxiv_bot')

obj = ArxivSearch(category, submissions = 'recent')
soup = read_HTML(obj.category, submissions=obj.submissions)
#%%
# Search for the <a> tag containing the specific date
date_to_find = arxiv_formatted_date(dates[-1])
print((date_to_find))
#%%
link = soup.find_all('a', string=date_to_find)
print(link)
# Extract the href attribute
if link:
    href_value = link['href']
    print(f'Found link: {href_value}')
else:
    print('Date not found in the HTML.')

