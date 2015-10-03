usage = '''
usage: python restore()
       (Execute from the ProgrammableServer dir.)
'''

import os, shutil

## initialize psdir ##

psdir = os.getcwd()

## restore expanderOrderings.json and config.py ##

shutil.copyfile(
    'py/expanderOrdering.original',
    'expanderOrdering.json'
)

shutil.copyfile(
     'py/config.original',
     'config.py'
)

print('Restoration complete.')
print(
'Warning! Restoration assumed:' +
'\n  only config.py and expanderOrderings.json have been altered.'
)

