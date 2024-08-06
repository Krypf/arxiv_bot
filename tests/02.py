import requests
from bs4 import BeautifulSoup

def scrape_arxiv(url: str) -> list[dict[str, str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    papers = []
    for item in soup.find_all('div', class_='meta'):
        title_tag = item.find('div', class_='list-title')
        authors_tag = item.find('div', class_='list-authors')
        arxiv_tag = item.find('a', title='Abstract')

        title = title_tag.text.replace('Title:\n          ', 'Title: ').strip() if title_tag else 'N/A'
        authors = authors_tag.text.replace('Authors:\n', '').strip() if authors_tag else 'N/A'
        arxiv_link = f"https://arxiv.org{arxiv_tag['href']}" if arxiv_tag else 'N/A'
        
        papers.append({
            'title': title,
            'authors': authors,
            'arxiv_link': arxiv_link
        })
    
    return papers

# Example usage
url = 'https://arxiv.org/list/hep-th/recent'
papers = scrape_arxiv(url)

for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {paper['authors']}")
    print(f"ArXiv Link: {paper['arxiv_link']}\n")
