import requests

base_url = 'http://export.arxiv.org/api/query?'
search_query = 'cat:hep-th'  # Category: High Energy Physics - Theory
start = 0
max_results = 10

query = f'search_query={search_query}&start={start}&max_results={max_results}'
response = requests.get(base_url + query)
print(response.text)
