#!/bin/sh
PATH=$HOME/.pyenv/shims:$PATH
# cd ~/arxiv_bot
python arxiv_bot/arxiv-save-HTML.py
sleep 5
python arxiv_bot/arxiv-save-text.py
sleep 5
python arxiv_bot/post-bluesky.py
sleep 5
python arxiv_bot/post-twitter.py
# echo "Done"