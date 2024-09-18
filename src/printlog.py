#%
from datetime import datetime

def printlog(log_message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{current_time}] {log_message}"
    with open('log.txt', 'a') as file:
        file.write(log_entry + '\n')
    return None