'''
The shutdown mixin is for use by the shutdown expander.  

It provides a shutdown function which will shut the server down if running in localServe mode
'''

def _do_shutdown(handler):
   from config import localServe
   if localServe: 
      handler.send_error(
       202,
       ( 'Server Shutdown By Request! ' +
         '(Ignore offline processing claim.)' )
      )
      handler.server._MEM['want_continue'] = False
      raise Handled

def getResources(handler):
    return dict(
      shutdown = (lambda : _do_shutdown(handler))
    )

