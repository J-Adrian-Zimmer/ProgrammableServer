'''
The out mixin provides

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

   page_out -- creates an html page with these parameters and
               their defaults
      title = 'anonymous'
      jsList = []
      cssList = []
      other_head = ''
      body = ''
  
      these are put into a page template that includes
        jQuery as defined in config.py

   dbg -- may write its argument on console
          (see debug in config.py)
   
'''

from urlparse import urlparse

def getResources(handler):
   sc = handler.server.soconsts
   return dict( 

      send = 
        lambda status, headers, contents:
           _send_(handler,status,headers,contents),

      giveup = lambda who,status,message: \
                   _giveup_(handler,who,status,message),

      page_out = ( lambda title = 'anonymous',  
                          jsList = [],
                          cssList = [],
                          other_part = '',
                          body = '':
                           _page_out(             # adds handler 
                                handler,
                                title,
                                jsList,
                                cssList,
                                other_part,
                                body
                           )
                 ),
   
      dbg = sc.dbg
   
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
   raise Handled()
 
def _giveup_( handler, who, status, message ):
   handler.send_error(
          status,
          "\n  " + who + ":\n  " + message
   )
   print( who + ' giving up!\n  ' + message)
   raise Handled()

def _page_out(handler,title,jsL,cssL,otherH,body):
   from config import jquery
   js = ''.join(
             map( 
              lambda x: _js_template % x, 
              [jquery] + jsL  
           ))
   css = ''.join(
             map( 
              lambda x: _css_template % x, 
              cssL 
          ))
   page = (_startPage_template.format(
              title = title,
              js = js,
              css = css,
              other_head = otherH,
              body = body
          ))
   handler.send_response(200)
   handler.send_header("content-type","text/html")
   handler.send_header(
       'content-length',
       len(page.encode('utf-8'))
   )
   handler.end_headers()
   handler.wfile.write(page)
   raise Handled

_startPage_template = """
<!doctype html>
<!-- generated with Python's string format from a template -->
<html>
<head>
<title>{title}</title>
<meta charset="utf-8"/>

<!-- css links -->
{css}

<!-- javascript source files -->
{js}

<!-- other head tags, incl. <script> & <style> -->
{other_head}

</head><body>
{body}
</body></html>
""" 
   
_js_template = """
<script language="javascript" type="text/javascript" src="%s"></script>
"""

_css_template = """
<link rel="stylesheet" type="text/css" href="%s"/>
"""
 

