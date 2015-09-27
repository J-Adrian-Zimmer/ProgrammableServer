'''
The shutdown mixin is for use by the shutdown expander.  

It provides a shutdown function which will shut the server down if running in localServe mode
'''

def _do_shutdown(handler):
  ip = handler.client_address[0]
  if ip[:9]=='127.0.0.1':
    handler.send_error(
      202,
      ( 'Server Shutdown By Request! ' +
        '(Ignore offline processing claim.)' )
    )
    handler.server.soconsts.want_continue = False
    raise Handled

def getResources(handler):
    return dict(
      shutdown = (lambda : _do_shutdown(handler))
    )

