## This expander has a post method responds to an 
## Ajax request.  
## The request came as a plain string coded in JSON
## format.
## jsonIn gets that JSON as a Python object for us
## json_out converts a Python dict to JSON and 
## sends it back to the browser.

## Again: incoming is Python object
##        outgoing is Python dict

## Both jsonIn and json_out are provided by jsonSupport

def post():
  using('basic','jsonSupport')
  if path=='/echoHandler':
     jsn = jsonIn()
     if jsn.goal=='uppercase':
        json_out( { "text" : jsn.text.upper() } )
     else:
        json_out( { "text" : jsn.text.lower() } )


