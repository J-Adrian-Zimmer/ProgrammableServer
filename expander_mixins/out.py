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
'''

from urlparse import urlparse

def getResources():
   return dict( 
      send = _send_,
      giveup = _giveup_,
      page_out = _page_out
   )

## helpers ##

def _page_out(
      title = 'anonymous',
      jsList = [],
      cssList = [],
      other_head = '',
      body = ''
):
   # set Javascript links, starting with jquery
   jq = (unmixed('localInfo')).jquery
   js = ( _js_template_foreign % jq  
                      if jq[0:4]=='http' 
                      else _js_template % jq )
   js += ''.join(
             map( 
              # wrap jquery and each js file in jsList
              
              lambda x: _js_template % x, 
              jsList 
           ))
   
   # set CSS links   
   css = ''.join(
             map( 
              # wrap each css file in cssList
              lambda x: _css_template % x, 
              cssList
          ))
   page = (_startPage_template.format(
              title = title,
              js = js,
              css = css,
              other_head = other_head,
              body = body
          ))
   handler.send_response(200)
   handler.send_header(
      "content-type","text/html"
   )
   handler.send_header( 'content-length', str(len(page)) )
   handler.end_headers()
   handler.wfile.write(page)
   raise Handled

def _send_(  status, headers, contents ):
   handler.send_response(status)
   if not (headers and headers.has_key('content-length')):
      headers['content-length'] = str(len(contents))
   for k in headers:
      handler.send_header(k,headers[k])
   handler.end_headers()
   handler.wfile.write( contents )
   raise Handled()
 
def _giveup_(  who, status, message ):
   import sys
   sys.stderr.write(
      who + ' giving up!\n  ' + message +'\n'
   )
   print(
      who + ' giving up!\n  ' + message +'\n'
   )
   handler.send_error( status, message )
   raise Handled()


_startPage_template = """
<!doctype html>
<!-- generated with Python's string format from a template -->
<html>
<head>
<title>{title}</title>

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
<script language="javascript" type="text/javascript" src="/js/%s"></script>
"""

_js_template_foreign = """
<script language="javascript" type="text/javascript" src="%s"></script>
"""

_css_template = """
<link rel="stylesheet" type="text/css" href="/css/%s"/>
"""
 

