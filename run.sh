#!/bin/sh
set -e # Exit immediately if a command exits with a non-zero status
export PATH=$HOME/.pyenv/shims:$PATH
# sh ~/auto/wifi/tethering.sh
sleep 1
python main.py