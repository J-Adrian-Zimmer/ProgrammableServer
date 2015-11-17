# ProgrammableServer

(This will be upgraded to the version in develop Very Soon Now. See the README.md for an overview of what's coming.)

If you are a Python programmer wanting to set up a server for your
own application,  if you don't need a high volume, general purpose
server and are put off by the complexities of Apache and
BaseHTTPServer, then ProgrammableServer may be for you.  It is easy
to setup and, if necessary, reconfigure.

With ProgrammableServer, you can create a simple or complex
application whose demands on a web server are few.  You do this by
writing one or more *expanders* each of which handles a single kind
of request.  Writing an expander is made easier because you have a
choice of mixins to include.  An expander mixin consists of a few
functions that provide an environment customized to your needs.

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
serve a file from the directory tree determined in the configuration
file `config.py`.  If a POST request then a "not found" message is
sent.

The `config.py` file is also used to set up separate expander lists
for GET and POST requests.

You can set up the ProgrammableServer and run the example expander
applications this way

1. install Python 2.7
2. download and unzip this application
3. run serve.py 

If your computer is set to run Python 2.7 on `.py` files, you can
just click on `serve.py`.  By default it will run with `localServe` set to
`True` and so will only serve browsers on the same computer.

The sample applications are

**shutdown** (localhost/shutdown)

> Shuts the server down (only works when `localServe` is `True`)

**echo** (localhost/echo)

> An example whose source code shows how to set up
> Ajax/JSON communication with the server.  

**uploadPic** (localhost/uploadPic)

> An example which uploads jpg files;  the target directory is
> controllable through `config.py`.  The default sets it  to the
> `uploads` subdirectory of the directory containing `serve.py` 

> As with all these sample expanders, the real value to you from
this example comes
> from reading the source code so you will know how to make your
> own.

**showRequestParameters** (localhost/showRequestParameters...)

> An investigating application that shows the request path, a table of HTTP declarations, and a table
> of query string declarations.  You can expand the URL however you
> like, for example:  

> `localhost/showRequestParameters/onward?id=myself`

There are two other sample expanders in the GET list, `send_js_css` and
`countSimpleServes`, but if you try to get them with your browser you
will be told "File not Found".   This is because they do their thing
without actually handling the request and sending something to the
browser.

The `send_js_css` expander should appear in the GET list before any
expander you create.  What it does is serve up your Javascript and
css pages.  This is necessary because when your expander serves up a
page, SimpleHTTPRequestHandler will be skipped.  Thus some other
way to serve Javascript and css files for that page is needed.

The `countSimpleServes` expander is an example of how information
can be saved in the server state.  Saving information in the server
state enables information to be saved from one request to another.
The information saved by `countSimpleServes` is the number of times
SimpleHTTPRequestHandler has been used to serve a static page since
the server was started.  This
information is printed to the console window that pops up when
`serve.py` runs.

There are only two expanders in the POST list.  One talks to the `echo`
page with Ajax/JSON.  The other saves uploaded pictures. 
 
When an expander executes, a `using` function is installed into its global
space.  What `using` does is to allow mixins to be installed
into local spaces.  The mixins are located in the
`expander_mixins` directory and are well commented.  You can write
your own as well.

I am planning a 3 volume set of short, inexpensive ebooks about this software.
Volume I will be about writing expanders.  Volume II will be about
writing expander mixins.  Volume III will explain three nontrivial
applications.  They will be published by Bonsai Reads and they will
be available
through Amazon, Apple, Barnes & Noble, and others.

### Rant

Once upon a time there was a flurry of research into what consituted a good software module and how good software modules should interface with each other.

Then along came object-orientation with promises of encapsulation and inheritance that seemed to make that research obsolete.

The result has not been pretty. An object definition may describe methods for these purposes

- Object creation
- Object's external interface
- Object's internal methods
- Object's abstract internal methods to be defined in subclasses
- Object's defined abstract methods establishing superclass behavior.
- Object's redefined methods changing superclass behavior.
- Callback methods received as parameters.

Other lists of purposes could be compiled but this one makes the point.

The software community's response to this complexity has been to turn to the study of patterns. This has been helpful because a pattern is like a map that helps us understand complex terrain.

However a map does not simplify the terrain.  A pattern can simplify
the coding process but it does not necessarily simplify the code.  That only
happens when one takes the time to think about the design.

Python's SimpleHTTPRequestHandler is an example of a class with disparate methods from the class and its superclass. Extending it by subclassing would merely boil this mess over the container of the average mind.

The ProgrammableServer relies on a ProgrammableRequestHandler class
which is a subclass of SimpleHTTPRequestHandler that hides rather
than augments its complexity.

[J Adrian Zimmer](http://www.jazimmer.net)

