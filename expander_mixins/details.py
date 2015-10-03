'''
The details mixin provides

   command --  GET, POST, HEAD 
   url_query -- the query part of the url, parsed as a dict
   web_root -- the root directory from which 
               SimpleHTTPServer serves
   server_dir -- the directory serve.py is in
   localServe --  True, False or the IP number of a local 
                  network gateway
                  
                  False: requests from anyplace honored
                  True: only requests from same computer
                  IP number: requests from same network,
                     but not the gateway, honored
   path -- an array containing the parts of the 
           url path (each nonempty and with unwanted 
           chars removed)
   pathext -- the extension found in the path without the .
              (it is also a suffix of path[-1])
   headers -- http headers from request

Note:
 -- the unprocessed url path (sans query & fragment)
    is always available under the name, request
 -- the entire parsed url available in handler._MEM
    (see init_MEM in ProgrammableRequestHandler.py)
'''

import os, re

from urlparse import parse_qs 


def getResources(handler):
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
      web_root = cs.web_root,
      server_dir = cs.server_dir,
      localServe = cs.localServe,
      url_query = parse_qs(query),
      headers = handler._MEM['headers']
   
   )

