'''
Serves '/js/...' and '/css/...' files from the respective application or server subdirectories.  Most recently installed application has precedence.  Then the next most recently installed, etc.  

As a last resort, subdirectories of the server are attempted.  (This is not meant to encourage you to put things there.  Doing so will make server upgrades difficult for you.)
'''

def get():
   if request[:4]=='/js/':
      from os.path import isdir
      mixins('fileTools')
      file_out( search(request))
   elif request[:5]=='/css/':
      from os.path import isdir
      mixins('fileTools')
      file_out( search(request))

