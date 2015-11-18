# ProgrammableServer

If you are a Python programmer 

1. who wants to set up a server for your own applications,  

1. who doesn't need a high volume, general purpose server, and 

1. who is put off by the complexities of Apache and Python's
SimpleHTtPserver

then the ProgrammableServer may be for you.  It is easy
to setup and to write applications for.

With ProgrammableServer you can create a simple or complex
application provided the demands on a web server are few.  You do this by
writing one or more *expanders* each of which handles a single kind
of request. 
 
Web servers send browser requests to handlers for processing.  The
ProgrammableServer's handler expects each expander to look over
a request and then to do one of three things:

- handle the request
- report an error
- pass the request on to the next expander

In the first two cases, a response is sent and expanders further
down in your list of expanders are ignored.

If the expander list is exhausted without handling the request, then
what happens will depend on whether it is a GET or POST request.  If a
GET request then Python's SimpleHTTPRequestHandler takes over to
serve a file from the directory tree that is determined in the configuration
file `config.py`.  If a POST request then a "not found" message is
sent.

You can set up the ProgrammableServer this way

1. install Python 2.7
2. download and unzip this application
3. run serve.py 

If your computer is set to run Python 2.7 on `.py` files, you can
just click on `serve.py`.  By default it will only serve browsers on
the same computer.

The `config.py` file allows you to do such things as 

1. change the port being listened to
2. alter the server so it will accept requests from anywhere not
just from the local machine
3. change the directory from which static files are served
4. turn off the feature which lists the contents of directories

The `config.py` file is well commented.  You can start experimenting with
changes.  Of course the server needs to be restarted with each 
new round of changes.

The server can be halted by requesting this URL

`localhost/shutdown`

from a browser on the same computer as the server.

The Programmable Server is a skeleton on which applications are
built.  You cannot do much with a bare bones server that could not
be done with Python's SimpleHTTPRequestHandler.  To install a
demonstration application change to the `demo_app` subdirectory and
run `install.py`.  Then enter this URL 

*\<domain name or IP number\>*/about`

Of course, if you haven't edited the `config.py` file the URL must
be

`localhost/about`

The included demonstrations are not going to show you whizz-bang
gotta-have applications.  Their purpose is to explain how you, the
Python and Javascript programmer, will find your work made easier by
the Programmable Server.

Two capabilities of particular noteworthiness are 

1. the seamless transfer of data between a Javascript object on the
client and a Python object or dict on the server.  (See the `echo`
demo.)

2. the support for responsive web pages that is provided by a
Javascript function that fetches a CSS file from the server and
applies it to the current web page. (See the `uploadPic` demo.)

This kind of functionality is supported by middleware which exists
to make expanders easier to write.  This middleware comes in the
form of *expander mixins* (and a single Javascript support file).
An expander can choose the mixins whose functions it wants loaded in
the current namespace.

If the supplied expander mixins do not serve the needs of your
expanders, you can create your own and place them in applications.

The source code of all the included expanders, expander mixins, and
Javascript support files is fairly well documented.  These files
are not long and there are not many more than a dozen of them.  Many of
you can get up to speed by looking through their source code.

For others there is my forthcoming "A  Python Programmable Web
Server" ebooklet.  As with my "From Simple I/O to
Monad Transformers" this ebooklet will be available from Amazon in 
Kindle format and from many other sources in epub format.

[J Adrian Zimmer](http://www.jazimmer.net)


