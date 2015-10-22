'''
This expander has a post method responds to an Ajax request.  
The request comes in from the echo expander as a plain string 
coded in JSON format. This way

 """{ goal: <"uppercase" or "lowercase">,
      text: <user entered text>
    }"""

The jsonIn method translates such a string incoming string into a 
Python object.

The jsonOut method method translates a JSON string of this form

 """{ text: <transformed text>}"""

and sends it back to the browser.

NOTICE: Incoming is a Python object whereas outgoing is a 
        Python dict.
'''

## Both jsonIn and json_out are provided by jsonSupport

def post():
  if request=='/echoHandler':
     mixins('jsonSupport')  # for jsonIn and jsonOut
          # jsonSupport.py is found in expander_mixins
     jsn = jsonIn()
     if jsn.goal=='uppercase':
        json_out( { "text" : jsn.text.upper() } )
     else:
        json_out( { "text" : jsn.text.lower() } )


