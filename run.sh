#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status
PATH=$HOME/.pyenv/shims:$PATH
python arxiv_bot/main.py