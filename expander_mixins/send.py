'''
The send mixin has two functions.  One handles a request that has
no errors and the other returns error messages to the browser and
the log.  (The log by default written to the console.)
'''

def _send_( handler, status, headers, contents ):
   handler.send_response(status)
   if not (headers and headers.has_key('content-length')):
      headers['Content-Length'] = \
         str(len(contents.encode('utf-8')))
   for k in headers:
      handler.send_header(k,headers[k])
   handler.end_headers()
   handler.wfile.write( contents )
   raise handler.Handled()
 
def _giveup_( handler, status, message ):
   handler.send_error(status,message)
   raise handler.Handled()


def getResources(handler):

   return dict(
      
      # sends transfmits response and raises Handled
      send = lambda s,h,c: _send_(handler,s,h,c),
         # s : HTTP status
         # h : dict, e.g. { 'content-type': 'text/plain' }
         #     usually best to let us set 'content-length'
         # c : contents as described in h

      giveup = lambda s,m: _giveup_(handler,s,m)
         # s : HTTP status
         # m : error message
      
   )
   
