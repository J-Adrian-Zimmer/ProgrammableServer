'''
  The shudown expander shuts the server down if
  request from same computer 
'''

def get():
   if request=='/shutdown': 
      mixins( 
             'network' # for me
           )
      if me():
         (handler.server.soconsts.shutdown)()
         raise Handled()

