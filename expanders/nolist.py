'''
Include the nolist expander if you don't want the files in your
directories listed.
'''

from os.path import isdir,exists,join

def get():
   filepath = join(
      (unmixed('constants')).web_root,
      request[1:]
   )
   if ( isdir(filepath) and 
        not exists(join(filepath,"index.html")) 
   ): 
      (unmixed('out')).giveup( 'nolist', 404,
              "Cannot find " + request 
      )
