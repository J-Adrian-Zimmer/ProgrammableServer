#  response is a page that shows the path, query, and http
# information received by the server

def get():

   if request[:22]=='/showRequestParameters':
      # could use path=='showRequestParameters' (if
      # mixins loaded before the if)
      # but then mixins might unnecessarily be loaded
      mixins(
         'requestInfo',  # for path, headers, url_query, 
         'out'    # for send
      )  # requestInfo and out are found in expander_mixins

      def dictDisplayer( buildme, item ):
          return buildme + ( 
              "<tr><td>%s</td><td>%s</td></tr>" % item
          )

      html = html_template % dict(
          requesttype = command,
          path = ', '.join(path),
          httpstuff = dict_template % (
                         "The HTTP Key/Values",
                         reduce(
                            dictDisplayer,
                            headers.items(),
                            ''
                         )
                      ),
          querydict = dict_template % (
                         "URL Query as Key/Values Pairs",
                         reduce(
                            dictDisplayer,
                            url_query.items(),
                            ''
                         )
                      )
      )                           
     
      send(
         200,
         { 'content-type':'text/html; charset=utf-8' },
         html
      ) 

html_template = """
<!doctype html>
<!-- generated with Python's string format from a template -->
<html>
<head>
<title>Demonstrating ProgrammableRequestHandler's Basic Mixin</title>
<!-- css and css generators -->
<link rel="stylesheet" type="text/css" href="/css/showRequestParameters.css"/>
</head><body>
<center><h1>Available Request Details</h1>
<p>
Source code for this demo is found in
'demo_app/expanders/showRequestParameter.py`.
</p></center>
<div id="left">
   <h1>The Request Type</h1>
   <table><tr><td>%(requesttype)s</td></tr></table>
   <h1>The <code>path</code> array</h1>
   <table><tr><td>[%(path)s]</td></tr></table>
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
