# shuts the server down if in localServer mode
# see the shutdown mixin

def get():
   using('out')
   if request=='/shutdown': 
      (handler.server.soconsts.shutdown)()
      raise Handled()

