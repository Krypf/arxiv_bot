# arxiv_bot

This is a Python library for arXiv bots.

tests, arxiv_bot フォルダのスクリプトは 親フォルダから実行してください。  
Scripts in the tests folder must be run from the parent folder.

For example, 
```python
python tests/arxiv-bot-test.py gr-qc 2024-07-14 2024-07-21
```

ホームディレクトリに写すとコードが実行できます。（乗っ取りはやめてください。）


# Codes

## Flow

1. 'arxiv_bot/arxiv-save-HTML.py' によって New Submissions の HTML ソースをダウンロードします。
2. HTML フォルダのソースから Title, Authors, Link (abs, pdf) を抜き出します。
3. Bluesky にアップロードします。

## arXiv

物理分野の arXiv の更新は以下のように分類されています。

* Recent submissions
    * New submissions
    * Cross-lists
* Replacements

Bot は New submissions のみを Bluesky にアップロードします。  
The bot uploads only new submissions to Bluesky.

# Bluesky API

Bluesky ではデフォルトで API が使えるようになっています。~~Twitter と違って無料です。~~

You are free to use the Bluesky API by default. ~~It is perfectly free, unlike Twitter.~~

> Bluesky Documentation | Bluesky   
> https://docs.bsky.app/ 

Python で Bot を作ります。

> The AT Protocol SDK   
> https://atproto.blue/en/latest/ 

こちらも参考にしました。

> Creating a post | Bluesky  
> https://docs.bsky.app/docs/tutorials/creating-a-post 
> https://docs.bsky.app/docs/tutorials/creating-a-post#website-card-embeds

# arXiv API

arXiv にも API が用意されていますが、API よりも Web ページのソースを利用したほうが性能が良いので、main code では使わないつもりです。

> arXiv API Access - arXiv info  
> https://info.arxiv.org/help/api/index.html 


