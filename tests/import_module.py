#%% https://chatgpt.com/c/7e987fc0-91b5-4240-881b-df03af053070
import sys
import os

# Get the current directory of the test script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the arxiv_bot folder
arxiv_bot_dir = os.path.join(current_dir, '..', 'arxiv_bot')

# Add the arxiv_bot folder to the system path
sys.path.insert(0, arxiv_bot_dir)