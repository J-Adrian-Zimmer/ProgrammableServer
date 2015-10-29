#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Running Python from $PATH, it had better be Python 2.7.x

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

print('\nRestoration complete.')
print(
'  Only config.py and expanderOrderings.json have been altered.\n'
)

