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
    ajaxable_page : for GET requests
                 writes a page according to template 
                 below (defaults shown) 
                 
                 write_page arguments:
                     title =
                     jsList = []
                     cssList = []
                     other_head = ''
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

def getResources(handler):
   using('out')
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

   def ajaxable_page(
      title='anonymous',
      jsList=[],
      cssList=[],
      other_part='',
      body=''
   ):
      jsList = jsList + ["js/support.js"]
      page_out( title, jsList, cssList, other_part, body ) 

   return dict(
      jsonIn = jsonIn,
      json_out = json_out,
      ajaxable_page = ajaxable_page,
      giveup = giveup
   )




