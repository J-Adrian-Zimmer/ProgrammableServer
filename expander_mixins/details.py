'''
The details mixin provides

   handler --  the current request handler
   Handled --  the exception to raise when a
               request is handled
   url_query -- the query part of the url, parsed as a dict
   url_fragment -- the fragment part of the url
   web_root -- the root directory from which 
               SimpleHTTPServer serves
   path -- an array containing the parts of the 
           url path (each nonempty and with unwanted 
           chars removed)
        -- the unprocessed url path is in the basic mixin
           and is called 'request'
   pathext -- the extension found in the path without the .
              (it is also a suffix of path[-1])

DO NOT attempt to change anything here.
'''

import os, re
from config import unwanted_chars

from urlparse import parse_qs 


def getResources(handler):
   
   a,b,pathstr,c,query,fragment = urlparse(handler.path)
   
   pathts =  filter(
                lambda x: x!='',
                map(
                   lambda x: re.sub(unwanted_chars,'',x),
                   os.path.splitdrive(pathstr)[1].split('/')
                )
             )

   if len(pathparts)==0:
      ext = ''
   else:
      ext = os.path.splitext(pathparts[-1])[1][1:]

   return dict(
      
      path = paths,
      pathext = ext,
      web_root = handler.server.psdata['web_root']
      url_query = parse_qs(query),
      url_fragment = fragment,
      handler = handler,
      Handled = handler.server.psdata['Handled']
   
   )

