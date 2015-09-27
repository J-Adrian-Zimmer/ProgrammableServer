'''
The details mixin provides

   url_query -- the query part of the url, parsed as a dict
   url_fragment -- the fragment part of the url
   web_root -- the root directory from which 
               SimpleHTTPServer serves
   server_dir -- the directory serve.py is in
   localServe --  True, False or the IP number of a local 
                  netwowrkgateway
                  
                  False: requests from anyplace honored
                  True: only requests from same computer
                  IP number: requests from same network,
                     but not the gateway, honored
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

from urlparse import urlparse, parse_qs 


def getResources(handler):
   using('basic')
   
   unw = handler.server.soconsts.unwanted_chars
   a,b,pathstr,c,query,fragment = urlparse(handler.path)
   
   path =  filter(
                lambda x: x!='',
                map(
                   lambda x: re.sub(unw,'',x),
                   os.path.splitdrive(pathstr)[1].split('/')
                )
             )

   if len(path)==0:
      ext = ''
   else:
      ext = os.path.splitext(path[-1])[1][1:]

   cs = handler.server.soconsts

   return dict(
      
      path = path,
      pathext = ext,
      web_root = cs.web_root,
      server_dir = cs.server_dir,
      localServe = cs.localServe,
      url_query = parse_qs(query),
      url_fragment = fragment,
   
   )

