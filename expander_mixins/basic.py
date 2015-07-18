'''
The basic mixin adds references to the handler, the URL's path, and
the Handled Exception.
'''

from urlparse import urlparse, parse_qs

def getResources(handler):
   a,b,path,c,query,fragment = urlparse(handler.path)
   
   return dict( 

      # ref to the SimpleHTTPRequestHandler
      handler = handler,

      # path part of the URL 
      path = path,

      # Handled must raised to stop evaluation
      # of further expanders
      Handled =  handler.Handled
   )
   

