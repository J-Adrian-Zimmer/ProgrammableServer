## This expander demonstrates use of the set_web_root function.
## 
## It is not included in expanderOrderings.editable because its value
## is dubious.

def get():
   if request=='/toggle':
      mixins('localInfo','jsonConnect')
      spage_out(
          title="Toggling the Web Root Directory",
          body = body,
          jsList=['toggle.js'],
          other_head=script
          )


def post():
   from os.path import join
   if request=='/toggle':
      mixins('jsonConnect','localInfo')
      try:
         jsn = jsonIn()
         jsn.cmd  # making sure the incoming JSON has
                  # correct format
      except:
         giveup(
            "toggle.post",
            400,
            "bad request"
         )
      if jsn.cmd=='to demo':
         set_web_root( 
           join( server_dir, 'demo_app', 'public' )
         )
         jsonOut( { "result":"demo dir" })
      elif jsn.cmd=='to server':
         set_web_root( 'public' )
         jsonOut( { "result":"server dir" } )
      elif jsn.cmd=='query':
         try:
            web_root.index('demo_app')
            jsonOut( {"result":"demo dir"} )
         except:
            jsonOut( {"result":"server dir"} ) 
      else:
         giveup(
            "toggle.post",
            400,
            "browser seems to be confused: " + jsn.cmd
         )


body= """
<h2>
Checking web root status ...
</h2>
<p>
Source code for this demo is at
<code>demo_app/expanders/toggle.py</code>.
</p><p>
When loaded, this expander queries the server to see which directory
tree the static files are being served from: either 
either the server's public directory or the demo's public
directory.  It then offers to toggle this service to the <i>other</i> directory.
</p><p>
When the server's directory is being served, you can see
</p><code>
/media/Foliage.jpg
</code><p>
When the demo's directory is being served, you can see
</p><code>
/media/Cattails.jpg
</code><p>
When the demo's directory is being served, you can still see the
Foliage picture with this
</p><code>
/public/media/Foliage.jpg
</code>
"""

script = """
<script>
queryStatus()
</script>
"""

