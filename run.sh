#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status
PATH=$HOME/.pyenv/shims:$PATH
python arxiv_bot/main.py
# python arxiv_bot/save-HTML.py
# sleep 0.5
# python arxiv_bot/save-json.py
# sleep 0.5
# python arxiv_bot/post.py