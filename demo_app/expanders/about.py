'''
Sends a page built around demo_app/about_demo.body.
'''

def get():

   if request=='/about':
      from os.path import join, normpath
      afile = normpath(join( 
                 (unmixed('localInfo')).server_dir,
                      # thisi unmixed returns the 
                      # localInfo expander mixin
                 'demo_app',
                 'about_demo.body'
                      # our convention is that .htm 
                      # .htm contain only the HTML 
                      # body
      ))
      with open( afile, 'rb' ) as fo:
          body = fo.read().encode('utf-8')
          # make sure we are sending utf-8
          # even though we are running in Latin-1
          # (see the second line in serve.py)
      (unmixed('out')).pageOut(
               body = body,
               title = "Demo of Programmable Server"
      ) # unmixed returns the out expander mixin as 
        # an object
        # pageOut sends a page and raises Handled
        # so no more expanders will execute
      raw_input('STARTING requestInfo')
