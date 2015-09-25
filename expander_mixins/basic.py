'''
The basic mixin provides

   request -- this is the path part of the request url and 
              is used by expanders to decide if they want 
              to handle a request

   send -- sends a response when there has been no error
      status -- the http status
      header -- a dict with the http header entries
          header could be { 'content-type': 'text/plain' }
         (usually best to let send() set 'content-length')
      contents -- the contents as specified in the header

   giveup -- used to send and log error responses 
             (logging by default is written to stdout on
             the console)
      status -- http status
      message -- error message

   page_out -- creates an html page with these parameters
      title =
      js =
      css =
      body =
  
      these are put into a page template that includes
        jQuery as defined in config.py
'''

from urlparse import urlparse

def getResources(handler):
   a,b,path,c,query,fragment = urlparse(handler.path)
   
   return dict( 

      request = path,

      send = 
        lambda status, headers, contents:
           _send_(handler,status,headers,contents),

      giveup = lambda status,message: \
                   _giveup_(handler,status,message),

      page_out = 
         lambda title,js,css,body: 
            _page_out(handler,title,js,css,body)
   
   )

## helpers ##

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
   def page_out(title,css,js,body):
      from config import jquery
      page = (_startPage_template % jquery).format(
                 title = title,
                 css = css,
                 js = js,
                 body = body
             )
      handler.send_response(200)
      handler.send_header("content-type","text/html")
      handler.send_header(
          'content-length',
          len(page.encode('utf-8'))
      )
      handler.end_headers()
      handler.wfile.write(page)
      raise handler.Handled

def _page_out(handler,title,js,css,body):
   from config import jquery
   page = (_startPage_template % jquery).format(
              title = title,
              js = js,
              css = css,
              body = body
          )
   handler.send_response(200)
   handler.send_header("content-type","text/html")
   handler.send_header(
       'content-length',
       len(page.encode('utf-8'))
   )
   handler.end_headers()
   handler.wfile.write(page)
   raise handler.Handled

_startPage_template = """
<!doctype html>
<!-- generated with Python's string format from a template -->
<html>
<head>
<title>{title}</title>

<!-- css and css generators -->
{css}

<!-- javascript support -->
<script src="%s"></script>
{js}

</head><body>
{body}
</body></html>
""" 

   )
   

