#%%
file_name = 'tests/import_module.py'
with open(file_name, 'r') as file:
    script = file.read()
exec(script)
#%%
from arxiv_function import ArxivSoup, ArxivText, ArxivSearch
category = 'gr-qc'
obj = ArxivText(category, '2024-09-15')
search = ArxivSearch(category, 'new')
soup = ArxivSoup(search.read_HTML())
def test(soup):
    print(obj.date)
    num = '1'
    # print((soup.find_dt_and_dd(num)))
    # print((soup.cross_list_number()))
    # number_new_submissions = (soup).cross_list_number()
    # iterator = map(str, range(1, (number_new_submissions)))# start with 1
    # print([i for i in iterator])
    print(soup.get_one_article_text(num))
    # obj.append_to_path('h')

#%%
test(soup)
