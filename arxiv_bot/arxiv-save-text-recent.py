#%%
from arxiv_function import ArxivSearch, ArxivText, categories_content, read_inner_file, arxiv_formatted_date

# Sample HTML
category = categories_content[0]
dates = read_inner_file(file='date', folder='arxiv_bot')
date_to_find = arxiv_formatted_date(dates[-1])
obj = ArxivSearch(category, submissions = 'recent')
# print(obj.extract_skip_numbers(date_to_find))
# soup = obj.read_HTML()
# print('Wed, 4 Sep 2024' in soup.text)
#%%
obj = ArxivText(category, date_to_find)
soup = obj.read_HTML_soup('recent')

