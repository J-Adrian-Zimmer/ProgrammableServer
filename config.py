## See the MIT license for usage rules.                 ##

## Leave config.original unedited.  Edit config.py instead    ##

## if debug=0, no output 
##    debug=1, only show messages from expanders
##    debug=2, show all messages

debug = 0


## port determines which port the server listens on

port = '80'

## localServe determines which browsers can expect a response
##    localServe = True -- only requests from same computer 
##                      -- are honored
##    localServe = False -- any request is honored
##    localServe = <gateway IP number> 
##                 -- Use this option only if you have a local
##                 -- net with netmask 255.255.255.0 and with
##                 -- just one gateway.
##                 -- Enter the IP/4 number of the gateway and
##                 -- requests coming from elsewhere in your
##                 -- local net will be honored.

localServe = True


## jQuery determines where jQuery comes from
## (default depends on localServe)

if localServe!=False:
   jquery = "/js/jquery.min.js"
else:
   jquery = \
   "https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js" 

#  You may have to edit the google reference or copy another 
#  jQuery into /js/jquery.min.js in the future.


## web_root is the root of the directory tree from which
## SimpleHTTPServer will serve -- it must be 'public'
## or the absolute path name of a directory

web_root = 'public'


## multithreading

multithreading = True


## to defang incomming path names these characters are
## often removed from all components -- written as a regular
## expression

unwanted_chars = \
   r'\.\.|\s|\\|\:|\(|\)|\[|\]|\{|\}|\)|\(|\?|\#'


############################################################

#   ProgrammableHTTPServer is expandable, you can write your
#   own expanders and expander_mixins.  You can also
#   add to this configuration file here.  


