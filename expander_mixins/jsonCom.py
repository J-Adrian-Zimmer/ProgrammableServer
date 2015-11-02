'''
   The jsonSupport mixin is much like the out mixin but
   subtracts the send function and adds others supporting
   applications that use Ajax (without the 'x', i.e. XML and
   with JSON) to communicate.
   Has these functions

      jsonIn --  for a POST request response to Ajax
                 Python object is obtained
      jsonOut -- for a POST request response to Ajzx
                 send a Ajaxable Pyton object or dict
      spage_out -- like out's page_out but adds 
                 Javascript for sending a JSONable
                 Javascript object via Ajax
      giveup -- the give from the out mixin
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
   mixins('out')  # for page_out and giveup
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

   def spage_out(
      title='anonymous',
      jsList=[],
      cssList=[],
      other_part='',
      body=''
   ):
      jsList = jsList + ["support.js"]
      page_out( title, jsList, cssList, other_part, body ) 

   return dict(
      jsonIn = jsonIn,
      jsonOut = jsonOut,
      spage_out = spage_out,
      giveup = giveup
   )
