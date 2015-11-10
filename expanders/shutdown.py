'''
  The shudown expander shuts the server down if
  request from same computer 
'''

def get():
   if request=='/shutdown':
      if (unmixed('requestInfo')).client_ip=='127.0.0.1':
         (handler.server.soconsts.shutdown)()
         raise Handled()

