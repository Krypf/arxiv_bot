#%%
from datetime import datetime
import arxiv_function
#%%
#%% constants
categories_content = arxiv_function.read_categories_file()
category = categories_content[0]

today = datetime.now().strftime('%Y-%m-%d')

# スクリプトを実行
arxiv_function.fetch_arxiv(category, today)
