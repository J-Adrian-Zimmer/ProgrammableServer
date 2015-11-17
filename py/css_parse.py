"""
Simplistic translation of css files to JSON

   parse_css(absfilepath) -- simple parsing of css
           
            css files must repeat this pattern without
            blank lines
             
                x {
                  ...
                }

            x can be tag name, id name (with #) or 
              class name (with .)

            ... is some repetition of 
                  property: value;
            one per line
            blank spaces within line optional
            property name chars are alphameric _ or - 
"""

def parse_css(absfilepath):
   import re

   pat1 = r'\s*((|\.|\#)[\w\-]+|)\s*\{\s*\n'
   pat2 =  r'\s*([\w\-]+)\s*:\s*([^;]+);\s*\n'
   pat3 = r'\s*\}\s*(\n|$)'
   pat4 = r'\s*\n?$'

   def state1( fi, jsnable ):
     line = fi.readline()
     if line=='':  return
     mob = re.match(pat1,line) 
     if mob:
        key = mob.group(1)
        jsnable[key] = {}
        state2( fi, key, jsnable )
     else:
        giveup(
           'css2json.parse_css',
           417,
           'new css declaration expected'
        )

   def state2( fi, key, jsnalbe ):
     line = fi.readline()
     mob = re.match(pat2,line)
     if mob:
        jsnable[key][mob.group(1)]=mob.group(2)
        state2( fi, key, jsnable )
     elif re.match(pat3,line):
        state3( fi, jsnable )  # maybe the end
     else:
        giveup(
           'css2json.parse_css',
           417,
           'bad css declaration'
        )

   def state3( fi, jnsable ):
     line = fi.readline()
     mob = re.match(pat1,line)
     if mob:                   # wasn't the end 
        key = mob.group(1)
        jsnable[key] = {}
        state2( fi, key, jsnable )
     elif re.match(pat4,line):
        return jsnable

   ## getting down to it ##

   with open(absfilepath,'r') as fi:
       jsnable = {}
       state1( fi, jsnable )
       return jsnable

if __name__=='__main__':

   s = """{".a": {"color": "white", "background": "black"}, "b": {"width": "27px", "height": "27px"}, "#x": {"display": "none"}}"""       
  
   import os,json

   psd = parse_css( 
          os.path.join( os.getcwd(), 'test.css' )
         )

   assert s==json.dumps(psd)
   print "Test Passed"


   
