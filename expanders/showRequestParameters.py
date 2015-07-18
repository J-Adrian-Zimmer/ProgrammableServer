#  response is a page that shows the path, query, and http
# information received by the server

def makeResponse():
   using('inparameters','parsepath','send')

   def dictDisplayer( display, item ):
       return display + ( 
           "<tr><td>%s</td><td>%s</td></tr>" % item
       )

   html = html_template % dict(
       requesttype = command,
       pathparts = ', '.join(pathparts),
       httpstuff = dict_template % (
                      "The HTTP Key/Values",
                      reduce(
                         dictDisplayer,
                         httpdict.items(),
                         ''
                      )
                   ),
       querydict = dict_template % (
                      "URL Query as Key/Values Pairs",
                      reduce(
                         dictDisplayer,
                         querydict.items(),
                         ''
                      )
                   )
   )                           
  
   if pathparts[0]=='showRequestParameters': 
      send(
         200,
         { 'content-type':'text/html; charset=utf-8' },
         html
      ) 

def get():
   makeResponse()


def post():
   makeResponse()


html_template = """
<!doctype html>
<!-- generated with Python's string format from a template -->
<html>
<head>
<title>Demonstrating ProgrammableRequestHandler's Basic Mixin</title>
<!-- css and css generators -->
<link rel="stylesheet" type="text/css" href="/css/showRequestParameters.css"/>
</head><body>
<div id="left">
   <h1>The Request Type</h1>
   <table><tr><td>%(requesttype)s</td></tr></table>
   <h1>The <code>pathparts</code> array</h1>
   <table><tr><td>[%(pathparts)s]</td></tr></table>
   %(querydict)s
</div>
<div id="right">
   %(httpstuff)s
</div>
</body></html>
""" 

dict_template = """
<div>
  <h1>%s</h1>
  <table>
     <tr><th>key</th><th>value</th></tr>
     %s
  </table>
</div>
"""
