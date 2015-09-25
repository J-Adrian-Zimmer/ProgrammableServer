'''
The parsepath mixin parses the URL's path and returns an array
of its components.  Each component has been defanged by removing
all the characters found in `config.py`'s `unwanted_chars` regular
expression.  Empty components have then been removed.

For most requests the array will simply be a list of components
found by separating with the operating system separator and
removing any drive letter.

Beyond the pathparts array, this mixin provides a pathext
string which is either empty or the extension of the 
request path (sans the period).
'''

import os, re
from config import unwanted_chars

from urlparse import parse_qs 

def getResources(handler):
   using('basic')
   
   pathparts =  filter(
                   lambda x: x!='',
                   map(
                      lambda x: re.sub(unwanted_chars,'',x),
                      os.path.splitdrive(path)[1].split('/')
                   )
                )

   if len(pathparts)==0:
      ext = ''
   else:
      ext = os.path.splitext(pathparts[-1])[1][1:]

   return dict(
      
      # pathparts is an array of the request path's
      # components; with operating system delimeters,
      # colins, parentheses and empty components
      # removed
      pathparts = pathparts,

      # extension is the path extension 
      # (the part of pathparts[-1] after the last period)
      pathext = ext
       
   )

