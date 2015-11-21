"""
The css2json expander is meant to respond to a request from get_css (find in js/support.js).  The functionality supported is the fetching and application of CSS files under Javascript control.

There is a severe limitation of the CSS selectors that can be used.
See `py/css_parse.py` for details.
"""

def post():
   if request=='/css_response':
      mixins('connect','fileTools')
      from css_parse import parse_css
           # css_parse is in the py subdirectory
      
      ## find the desired CSS file
      jsn = jsonIn()
      filename = search( jsn.css_path_name )
      
      ## read, parse into JSON form, and send
      ## to the client
      try:
        parse_css(filename)
        jsonOut( parse_css(filename) )
      except Handled:
        raise Handled()
      except:
        giveup(
           'css2json.post',
           404,
           'cannot find ' + jsn.css_file_name
        )

