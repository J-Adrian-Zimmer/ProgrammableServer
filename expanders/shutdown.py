'''
  The shudown expander shuts the server down if
  request from same computer 
'''

def get():
   if request=='/shutdown': 
      if (unmixed('network')).me():
         (handler.server.soconsts.shutdown)()
         raise Handled()

