'''
The jsonSupport mixin is a set of support functions for 
applications that use ajax and json to communicate 
between existing web pages and the server

the dict's members are

    jsonIn : gets the json sent in a POST request
                      json represented as Python object
    json_out : sends json response to a POST request
                 argument is a jsonable Python dict
                 (note!! jsonIn:object json_out:dict)
    page_out : for GET requests
                 writes a page according to template 
                 below  
                 
                 write_page arguments:
                     title =
                     js =
                     css =
                     body =

               template includes jQuery and a Javascript 
               json_out function whose arguments are
                     json-able object
                     callback for processing response
                     
               the callback's single argument is
                     a javascript object representation 
                     of a json

'''

import os, json

class _Bunch:
   '''
   The _Bunch class makes a Python class from a dict
   It enable jsonIn to return an object rather than a dict
   '''
   def __init__(self, adict):
        self.__dict__.update(adict)

def _giveup_( handler, status, message ):
   handler.send_error(status,message)
   raise handler.Handled()

def getResources(handler):
  
   def jsonIn():
      try:
        ln = int(handler.headers['content-length'])
        content = handler.rfile.read(ln)
      except:
        content = '' 
      return _Bunch(json.loads(content))

   def json_out(jsonable):
      contents = json.dumps(jsonable)
      handler.send_response(200)
      handler.send_header("Content-Type","text/plain")
      handler.send_header(
          'Content-Length',
          len(contents.encode('utf-8'))
      )
      handler.end_headers()
      handler.wfile.write(contents)
      raise handler.Handled

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

   return dict(
      jsonIn = jsonIn,
      json_out = json_out,
      page_out = page_out,
      giveup = lambda s,m: _giveup_(handler,s,m)
   )


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
<script src="/js/support.js"></script>
{js}

</head><body>
{body}
</body></html>
""" 

def console(msg):  # for debugging
   import sys
   sys.stderr.write(msg + '\n')


