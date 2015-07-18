'''
The server_state mixin lets you work with a dict that persists
as long as the server is running.
'''

def _save_state_(id,x):
   global state
   state[id] = x
   return x

def _get_state_(id):
   global state
   if state.has_key(id):
      return state[id]
   else:
      return None

def _clear_state_():
   global state
   state = {}

def getResources(handler):
  global state
  state =  handler.server._MEM['state']

  return dict(
     
    # save_state a message for later expanders working
    # with same request
    save_state = _save_state_,

    # get saved state
    get_state = _get_state_,

    # clear the server state
    clear_state = _clear_state_
  
  )


