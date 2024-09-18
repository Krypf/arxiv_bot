#%% https://chatgpt.com/c/7e987fc0-91b5-4240-881b-df03af053070
import sys
import os

# Get the current directory of the test script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the core folder
core_dir = os.path.join(current_dir, '..', 'core')

# Add the core folder to the system path
sys.path.insert(0, core_dir)