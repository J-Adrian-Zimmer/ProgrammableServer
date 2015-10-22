'''
The requestInfo mixin provides

   command --  GET, POST, HEAD 
   path -- an array containing the parts of the 
           url path (each nonempty and with unwanted 
           chars removed)
   pathext -- the extension found in the path without the .
              (it is also a suffix of path[-1])
   url_query -- the query part of the url, parsed as a dict
   headers -- http headers from request

Note:
 -- the unprocessed url path (sans query & fragment)
    is always available with the 'request' identifier
 -- search for init_MEM in ProgrammableHandler.py
    to see how to get the results of standared Python
    parsing of the URL
'''

import os, re

from urlparse import parse_qs 


def getResources():
   cs = handler.server.soconsts
   unwanted = cs.unwanted_chars
   pathstr = handler._MEM['path']
   query = handler._MEM['query']
   
   path =  filter(
                lambda x: x!='',
                map(
                   lambda x: re.sub(unwanted,'',x),
                   os.path.splitdrive(pathstr)[1].split('/')
                )
             )

   if len(path)==0:
      ext = ''
   else:
      ext = os.path.splitext(path[-1])[1][1:]


   return dict(
     
      command = handler.command, 
      path = path,
      pathext = ext,
      url_query = parse_qs(query),
      headers = handler._MEM['headers']
   
   )

