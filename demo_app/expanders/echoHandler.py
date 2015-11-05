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

## Both jsonIn and jsonOut are provided by jsonCom

def post():
  if request=='/echoHandler':
     mixins('jsonConnect')  # for jsonIn and jsonOut
          # jsonCom.py is found in expander_mixins
     jsn = jsonIn()
     if jsn.goal=='uppercase':
        jsonOut( { "text" : jsn.text.upper() } )
     else:
        jsonOut( { "text" : jsn.text.lower() } )


