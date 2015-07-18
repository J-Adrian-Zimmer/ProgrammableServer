'''
The dirs mixin adds directory references
'''

def getResources(handler):

  return dict( 
    
    # serverRoot is the directory containing serve.py,
    # config.py, the handler and the subdirectories 'js',
    # 'py, 'css', and 'upload'
    serverRoot = handler.server._MEM['serverRoot'],
    
    # serviceRoot is the directory from which 
    # SimpleHTTPServer serves,
    serviceRoot = handler.server._MEM['serviceRoot']

  )

