import requests
import sys

base_url = 'http://export.arxiv.org/api/query?'
category = sys.argv[1]
search_query = 'cat:' + category  # Category: High Energy Physics - Theory
start = 0
max_results = 10

query = f'search_query={search_query}&start={start}&max_results={max_results}'
response = requests.get(base_url + query)
print(response.text)
