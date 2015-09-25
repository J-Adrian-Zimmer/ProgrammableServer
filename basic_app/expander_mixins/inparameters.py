'''
The inparameters mixin adds references to dicts of query string
declarations and http declarations.  It also includes everything
from the basic mixin.
'''

from urlparse import urlparse, parse_qs

def getResources(handler):
   a,b,path,c,query,fragment = urlparse(handler.path)
   
   return dict( 

      # ref to the SimpleHTTPRequestHandler
      handler = handler,

      # command (GET, PUT, etc)
      command = handler.command,

      # path part of the URL 
      path = path,

      # query string part of the URL (or '')
      querydict = parse_qs(query),

      # dict of HTTP declarations
      httpdict = handler.headers,

      # Handled must raised to stop evaluation
      # of further expanders
      Handled =  handler.Handled
   )
   

