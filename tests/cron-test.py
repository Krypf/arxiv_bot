#%%
file_name = 'tests/import_module.py'
with open(file_name, 'r') as file:
    script = file.read()
exec(script)
#%%
from core.printlog import printlog

printlog('this is a cron test, this is a cron test.')
