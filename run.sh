#!/bin/sh
# set -e # Exit immediately if a command exits with a non-zero status
# sh ~/auto/wifi/tethering.sh
export PATH=$HOME/arxiv_bot/.venv/bin:$PATH
sleep 1
python main.py
sleep 1
sh shell/arxiv_start.zsh