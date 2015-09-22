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

## if debug=0, no output 
##    debug=1, only output from expanders
##    debug=2, all output

debug = 0


## web_root is the root of the directory tree from which
## SimpleHTTPServer will serve -- it must be 'public'
## or the absolute path name of a directory

# web_root = 'public'
web_root = 'c:/users/jaz/tmp'


## to defang incomming path names these characters are
## often removed from all components -- written as a regular
## expression

unwanted_chars = r'\.\.|\s|\\|\:|\(|\)|\[|\]|\{|\}|\)|\(|\?|\#'


## appDirs lists the application directories, each of which
## is expected to have expanders, expander_mixins, js, and
## css subdirs -- the directory containing serve.py 
## will be appended to the end of this list

appDirs = ['e:/git/ProgrammableServer/test_app']

## ProgrammableHTTPServer is expandable, you can write your
## own expanders and expander_mixins.  You can also
## add to this configuration file here.  Anything in 
## server.py's directory or the subdirectories, expander
## and expander_mixin can be imported by the python
## write.  See the MIT license for usage rules.


## for uploadPic expander

upload_dir = 'c:/users/jaz/tmp'


