import requests
from bs4 import BeautifulSoup

def scrape_arxiv(url: str) -> list[dict[str, str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    papers = []
    for item in soup.find_all('div', class_='meta'):
        title = item.find('div', class_='list-title').text.replace('Title:\n          ', 'Title: ').strip()
        authors = item.find('div', class_='list-authors').text.replace('Authors:\n', '').strip()
        link = item.find('div', class_='list-identifier').a['href']
        
        papers.append({
            'title': title,
            'authors': authors,
            'link': link
        })
    
    return papers

# Example usage
url = 'https://arxiv.org/list/hep-th/recent'
papers = scrape_arxiv(url)

for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {paper['authors']}")
    print(f"Link: {paper['link']}\n")
