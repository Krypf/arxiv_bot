from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://arxiv.org/list/hep-th/recent')

# Example: Extract titles of recent papers
titles = driver.find_elements(By.CLASS_NAME, 'list-title')
for title in titles:
    print(title.text)

driver.quit()
