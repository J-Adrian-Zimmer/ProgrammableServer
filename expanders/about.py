'''
Serves up the public/index.html, even if web_root has been 
defined away from public.
'''

def get():
  # this is an expander that can serve a GET request

  if request=='/about':
    (unmixed('staticResponse')).sendPublic('index.html')
    
    # if the path part of the URL is '/about'
    # we will send index.html which is in the
    # server's public directory
     
    # unmixed returns a staticResponse expander mixin
    # as an object
