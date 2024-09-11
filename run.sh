#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status
PATH=$HOME/.pyenv/shims:$PATH
# cd ~/arxiv_bot
python arxiv_bot/arxiv-save-HTML.py
sleep 1
python arxiv_bot/arxiv-save-text.py
sleep 1
python arxiv_bot/post.py
# echo "Done"