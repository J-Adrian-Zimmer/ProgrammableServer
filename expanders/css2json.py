def post():
   if request=='/css_response':
      from css_parse import parse_css
      mixins('jsonConnect','fileTools')
      jsn = jsonIn()
      filename = search( jsn.css_path_name )
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

