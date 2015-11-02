'''
The requestInfo mixin provides

   command --  GET, POST, HEAD 
   path -- an array containing the parts of the 
           url path (each nonempty and with unwanted 
           chars removed)
   pathext -- the extension found in the path without the .
              (it is also a suffix of path[-1])
   url_query -- the query part of the url (after the ?), 
                parsed as a dict
   headers -- http headers from request

Note:
 -- the unprocessed url path (sans query & fragment)
    is always available with the 'request' identifier
 -- search for init_MEM in ProgrammableHandler.py
    to see how to get the results of standared Python
    parsing of the URL
 -- fragments, which indicate position within a web
    page are not sent by browsers to servers and so
    are not available here
'''

from os.path        import splitext
from re             import sub
from urlparse       import parse_qs 

from urllib import unquote

def splitPath():
  return filter( 
   lambda x: x!='', 
   sub( '\.\.', '', unquote(request) ).split('/') 
        # forget your OS this is the
        # divider used in URLs
  )
     
def getResources():
   query = handler._MEM['query']
   regx = (unmixed('constants')).drop_regex

   path =  filter(
             lambda x: x!='',
             map(
                 lambda x: sub(regx,'',x),
                 splitPath()
             )
           )

   if len(path)==0:
      ext = ''
   else:
      ext = splitext(path[-1])[1][1:].lower()


   return dict(
     
      command = handler.command, 
      path = path,
      pathext = ext,
      url_query = parse_qs(query),
      headers = handler._MEM['headers']
   
   )

