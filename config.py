## these expanders will be applied to get requests in the 
## order listed until one handles the request
## If no expander handles the request, 
## SimpleHTTPRequestHandler is run.

#     Except for the first two, these are useless except
#     as examples of what can be done.

getList = [ 'shutdown', 
            'send_js_css', 
            'echo',
            'showRequestParameters',
            'uploadPic', 
            'countSimpleServes' ]


## these expanders will be applied to post requests in the
## order listed until one handles the request

postList = ['echoHandler',
            'uploadPic', 
            'showRequestParameters' ]


## the server refuses requests from other computers if this
## is set to True

localServe = True


## the jsonSupport mixin handler needs jQuery

if localServe:
   jquery = "/js/jquery.min.js"
else:
   jquery = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js" 


## web_root is the root of the directory tree from which
## SimpleHTTPServer will serve -- it must be 'public'
## or the absolute path name of a directory

web_root = 'public'


## to defang incomming path names these characters are
## often removed from all components -- written as a regular
## expression

unwanted_chars = r'\.\.|\s|\\|\:|\(|\)|\[|\]|\{|\}|\)|\(|\?|\#'


## upload_dir is where uploads can happen it must be 'upload'
## or the absolute path name of a directory

upload_dir = 'upload'


## ProgrammableHTTPServer is expandable, you can write your
## own expanders and expander_mixins.  You can also
## add to this configuration file here.  Anything in 
## server.py's directory or the subdirectories, expander
## and expander_mixin can be imported by the python
## write.  See the MIT license for usage rules.

