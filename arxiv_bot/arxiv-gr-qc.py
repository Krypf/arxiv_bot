#%%
import arxiv
from datetime import datetime
from .arxiv_function import get_results, save_text_append, fetch_arxiv
#%% constants
category = 'gr-qc'
today = datetime.now().strftime('%Y-%m-%d')
date = '2024-07-25'

# スクリプトを実行
fetch_arxiv(category, date)
