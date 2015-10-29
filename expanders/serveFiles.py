'''
This expander serves '/public/...' files from the respective server diirectory.  These files must have a standard, informative extension.  

(The image in /public/index.html is served this way because if the
serving were left up to the SimpleHTTPRequestHandler then it
wouldn't work if the web_root parameter were changed.)

Also serves '/js/...' and '/css/...' files from the respective application or server subdirectories.  These files must have extensions matching their directory names.   Most recently installed application has precedence.  Then the next most recently installed, etc.  Last in precedence are the '/js/...' and '/css/...' files in the server directory.

(Javascript and CSS files are served this way so they can be defined
in their corresponding applications and not necessarily placed in
the web_root directory.)
'''

def get():
   if request[:8]=='/public/':
      (unmixed('staticResponse')).sendPublic(
                                       request[8:]
                                  )
   elif request[:4]=='/js/':
      (unmixed('staticResponse')).sendSearch(
                                       request[4:],
                                       'js'
                                  )
   elif request[:5]=='/css/':
      (unmixed('staticResponse')).sendSearch(
                                       request[5:],
                                       'css'
                                  )
         
