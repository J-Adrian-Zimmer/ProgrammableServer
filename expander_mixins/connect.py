'''
   The connect mixin is much like the out mixin but
   subtracts the send function and adds others supporting
   applications that use jQuery's Ajax.
   
   Has these functions

      jsonIn --  use in a post() function that responds
                 to a request from JSON from json_out; 
                 returns a Python object matching the 
                 received JSON
      jsonOut -- use in a post() function that replies
                 to a json_out request;  sends a JSON
                 string made from a Python object or
                 dict
      pageOut -- use to make a page that will be 
                 communicating with JSON;
                 like out's pageOut but loads support.js
      giveup  -- taken from the out mixin

  The above functions work with these three functions from 
  support.js:

      json_out -- converts a Javascript object to JSON
                  and sends to the server via Ajax
      file_out -- uses a file loading template to send
                  a file to the server via Ajax; no form
                  is involved

  The page you build with pageOut must use upload.py if it
  is to upload a file.
'''

import os, json

class _Bunch:
   '''
   The _Bunch class makes a Python class from a dict
   It enables jsonIn to return an object rather than a dict
   '''
   def __init__(self, adict):
        self.__dict__.update(adict)

def getResources():
   out = unmixed('out')  
   def jsonIn():
      try:
        ln = int(handler.headers['content-length'])
        content = handler.rfile.read(ln)
      except:
        content = '' 
      return _Bunch(json.loads(content))

   def jsonOut(jsonable):
      contents = ( json.dumps(jsonable.__dict__) if 
             type(jsonable).__name__=='instance' else
                            json.dumps(jsonable) 
      )
      handler.send_response(200)
      handler.send_header("Content-Type","text/plain")
      handler.send_header(
          'Content-Length',
          len(contents.encode('utf-8'))
      )
      handler.end_headers()
      handler.wfile.write(contents)
      raise Handled

   def pageOut(
      title='anonymous',
      jsList=[],
      cssList=[],
      other_head='',
      body=''
   ):
      jsList = jsList + ["support.js"]
      out.pageOut( title, jsList, cssList, other_head, body ) 

   return dict(
      jsonIn = jsonIn,
      jsonOut = jsonOut,
      pageOut = pageOut,
      giveup = out.giveup
   )
