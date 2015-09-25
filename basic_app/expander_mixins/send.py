'''
The send mixin has three functions.  One handles a request that has
no errors.  Another returns error messages to the browser and the log, 
(By default, the log is written to the console.)

The third function is this page_out which writes a page according
the template below. Use these named arguments:

      title =
      js =
      css =
      body =

The template includes jQuery as defined in config.py.

'''

def getResources(handler):

   return dict(
      
      send = 
        lambda status, headers, contents:
           _send_(handler,status,headers,contents),
        # headers could be { 'content-type': 'text/plain' }
        #   (usually best to let send() set 'content-length')
        # contents is http contents as described in headers

      giveup = lambda s,m: _giveup_(handler,s,m),
         # s : HTTP status
         # m : error message

      page_out = 
         lambda title,js,css,body: 
            _page_out(handler,title,js,css,body)
   
   )

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

