# arxiv_bot

This is a Python library for arXiv bots.

tests, arxiv_bot フォルダのスクリプトは 親フォルダから実行してください。  
Scripts in the tests folder must be run from the parent folder.

For example, 
```python
python tests/arxiv-bot-test.py gr-qc 2024-07-14 2024-07-21
```

# Codes

1. 'arxiv_bot/arxiv-save-HTML.py' によって New Submissions の HTML ソースをダウンロードします。
2. HTML フォルダのソースから Title, Authors, Link を抜き出します。
3. Bluesky にアップロードします。


# Bluesky API

Bluesky ではデフォルトで API が使えるようになっています。

> Bluesky Documentation | Bluesky   
> https://docs.bsky.app/ 

Python で Bot を作ります。

> The AT Protocol SDK   
> https://atproto.blue/en/latest/ 

# arXiv API

arXiv にも API が用意されていますが、API よりも Web ページのソースを利用したほうが性能が良いので、main code では使わないつもりです。

> arXiv API Access - arXiv info  
> https://info.arxiv.org/help/api/index.html 


