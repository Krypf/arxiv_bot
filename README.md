# arxiv_bot

This is a Python library for arXiv bots.

tests, arxiv_bot フォルダのスクリプトは 親フォルダから実行してください。  
> Scripts in the tests folder must be run from the parent folder. For example, 
```python
python tests/arxiv-bot-test.py gr-qc 2024-07-14 2024-07-21
```

ホームディレクトリに写す (`git glone`) とコードが実行できます。（乗っ取りはやめてください。）

> You can run the code by copying it (`git glone`) into your home directory. (Please don't try to take over the system.)

# Codes

## Flow

1. New Submissions の HTML ソースをダウンロードします。
2. HTML フォルダのソースから Title, Authors, Link (abs, pdf) を抜き出します。
3. Bluesky にアップロードします。
4. Twitter にアップロードします。
5. Threads にもアップロードします（予定）。

---

1. Download the HTML source of "New Submissions". 
2. Extract the Title, Authors, and Link (abs, pdf) from the HTML folder source. 
3. Upload to Bluesky. 
4. Upload to Twitter. 
5. Upload to Threads (planned).

## arXiv

物理分野の arXiv の更新は以下のように分類されています。

> The arXiv submissions in the field of physics are categorized as follows

* Recent submissions
    * New submissions
    * Cross-lists
* Replacements

Bot は New submissions のみを Bluesky にアップロードします。  
> The bot uploads only new submissions to Bluesky.

# Bluesky API

☆☆成果物は[こちら](https://bsky.app/profile/krypf.bsky.social/lists/3kzls5tw2uw2t)☆☆

Bluesky ではデフォルトで API が使えるようになっています。~~Twitter と違って無料です。~~  
制限は `5,000 points per hour and 35,000 points` で、投稿は 1 時間で 約 1600 件（切り捨て）、1 日 約 11000件 可能なので ほとんど制限はないです。  
操作に対して以下のようにポイントが定められています。

* `CREATE	3 points`
* `UPDATE	2 points`
* `DELETE	1 point`

Python で Bot を作りました。ライブラリ名は AT Protocol といいます。

> ☆☆The outcomes are [here](https://bsky.app/profile/krypf.bsky.social/lists/3kzls5tw2uw2t)☆☆  
> You are free to use the Bluesky API by default. ~~It is perfectly free, unlike Twitter.~~  
> The limit is `5,000 points per hour and 35,000 points`, which is almost unlimited since you can submit about 1,600 posts in an hour (rounded down) and about 11,000 posts in a day.  
> The points are defined as follows for each operation.
> 
> * `CREATE	3 points`
> * `UPDATE	2 points`
> * `DELETE	1 point`
> 
> I created a Bot in Python. The library I used is called AT Protocol.


> **Reference**
> Bluesky Documentation | Bluesky   
> https://docs.bsky.app/  
> Rate Limits, PDS Distribution v3, and More | Bluesky  
> https://docs.bsky.app/blog/rate-limits-pds-v3  
> The AT Protocol SDK   
> https://atproto.blue/en/latest/  
> Creating a post | Bluesky  
> https://docs.bsky.app/docs/tutorials/creating-a-post  
> https://docs.bsky.app/docs/tutorials/creating-a-post#website-card-embeds


# Twitter API

☆☆成果物は [こちら](https://x.com/i/lists/1828539335723163734) です。☆☆

Twitter でも bot を作りました (version 1.0)。

Twitter の free bot が息絶えた 2023年5月以来、理論物理分野の arXiv bot は一部のカテゴリーを除いてありませんでしたが、この度復活させました。

Requirement は `tweepy` です。


> ☆☆The outcomes are [here](https://x.com/i/lists/1828539335723163734)☆☆  
> I have created a bot on Twitter as well (version 1.0).
> 
> Since May 2023, when Twitter's free bot died out, there had been no arXiv bot for theoretical physics except for a few categories, but we have now revived it.
> 
> The Requirement is `tweepy`.


> **Reference**
> X Developers  
> https://developer.x.com/en/portal/petition/essential/terms?plan=free  
> Tweepy https://www.tweepy.org/  
> tweepy/tweepy: Twitter for Python!  
> https://github.com/tweepy/tweepy 


# arXiv API

arXiv にも API が用意されていますが、API よりも Web ページのソースを利用したほうが性能が良いので、main code では使わないつもりです。

> The arXiv also supports an API, but we do not intend to use it in the main code because it is better to use the web page source rather than the API.


> arXiv API Access - arXiv info  
> https://info.arxiv.org/help/api/index.html 

# アメリカの休日 American Holidays

米国（アメリカ）の祝日・休日カレンダー 2024年  
https://holidays-calendar.net/calendar/usa_calendar.html 

# 手動の復旧メモ

arXiv や PC の不具合から手動で復旧（投稿）せざるをえないときのメモです。
5回更新以内であれば recent から復旧できます。

```
% python -m src.save-HTML --submissions recent --skip 0 --show 2000
% python -m src.save-json-recent txt
% python -m src.post --date txt

% python -m src.post_bluesky --date txt
```