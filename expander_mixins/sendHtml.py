'''
Provides one function, rwHtml, which
serves up a single page from a (whole HTML page) file whose
location is given as an absolute file name.

Useful to serve HTML from places outside the web_root tree.
'''

def _send(afile):
   send = (unmixed('out')).send
   with open( afile, 'rb') as fo: 
      page = (fo.read()).encode('utf-8')
   handler.send_response(200)
   handler.send_header(
      "content-type","text/html; charset=utf-8"
   )
   handler.send_header( 
      'content-length', str(len(page)) 
   )
   handler.end_headers()
   handler.wfile.write(page)
   raise Handled


def getResources():
   return dict( rwHtml = _send )
