#!/bin/sh
PATH=$HOME/.pyenv/shims:$PATH
# cd ~/arxiv_bot
python arxiv_bot/arxiv-save-HTML.py
# echo "0 "
sleep 5
python arxiv_bot/arxiv-save-text.py
# echo "0 "
sleep 5
python arxiv_bot/post-bluesky.py
# echo "Done"