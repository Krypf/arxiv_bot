#%%
from datetime import datetime
import arxiv_function
#%% constants
category = 'gr-qc'
today = datetime.now().strftime('%Y-%m-%d')

# スクリプトを実行
arxiv_function.fetch_arxiv(category, today)
