''' Put this expander last in config.py's getList and it will report
on the console how many times the SimpleHTTPRequestHandler has been
invoked since the server started operating.  '''

def get():
  using('server_state')
  if get_state('counter')==None:
     save_state('counter',1)
     print "First use of SimpleHttpRequestHandler"
  else:
     i = get_state('counter')
     i += 1
     save_state('counter',i)
     print "Use " + str(i) + " of SimpleHttpRequestHandler" 
