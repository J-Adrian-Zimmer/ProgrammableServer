# shuts the server down if in localServer mode
# see the shutdown mixin

def get():
   using('basic','shutdown')
   #  notice multiple mixins; one for handler.path and
   # one for shutdown()
   if path=='/shutdown': shutdown() 

