'''
This expander serves '/public/...' files from their the public directory.  These files must have a standard, informative extension.

Also serves '/js/...', '/css/...', and '/media/...' files from the respective application or server subdirectories.  These files must have extensions matching their directory names.   Most recently installed application has precedence.  Then the next most recently installed, etc.  

As a last resort, subdirectories of the server are attempted.  (This is not meant to encourage you to put things there.  Doing so will make server upgrades difficult for you.)
'''

def get():
   mixins('fileTools')
   if request[:4]=='/js/':
      file_out( search(request))
   elif request[:5]=='/css/':
      file_out( search(request))
   elif request[:8]=='/media/':
      file_out( search(request))
   elif request[:8]=='/public/':
      file_out(
          (unmixed('constants')).server_dir + request
      )
