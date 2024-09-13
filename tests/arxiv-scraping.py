#%% https://chatgpt.com/share/194eeabb-2adb-473e-a250-0ea75340cf4d
import requests
from bs4 import BeautifulSoup
# from arxiv_function import my_replace

url = 'https://arxiv.org/list/hep-th/new'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)
#%%
def my_replace(text: str) -> str:
    text = text.replace('Title:\n          ', 'Title: ')
    text = text.replace('\n        ', '\n')
    return text

# Example: Extract titles of recent papers
titles = [my_replace(title.text) for title in soup.find_all('div', class_='list-title')]
print(titles)