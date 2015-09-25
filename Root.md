Programmable Server
=========

There is not much you can do with this barebones server.  It is made to have apps plugged into it and its `config.py` file permits many customizations.  Here is a list of what is possible without any customization:

1.  Get this screen by entering the url `localhost` in your browser.
2.  Shut the server down by entering `localhost/shutdown` in your browser.
3.  See a bird picture by entering `localhost/media/webBird.JPG` in your browser.
4.  Add other things to the `public` subdirectory so you can see them the way you've seen the bird picture.

A first customization might be to search for `web_root` in `config.py` and set to a different directory.  This directory will become the root of your static file service.  The default is `public` which the server sees as a keyword telling it to use the default `public` subdirectory.  When you replace `public` be sure to use a full path name.  This  path name can point to anyplace on your computer you have access to.

A second customization might be to install the demonstration app on Github that shows how to program several things.  Install it this way

1. Download [this](https://github.com/j-adrian-zimmer/archives/...) zip fle.
1. Extract all the files and make note of the full path name of the directory containing `expanders`, `expander_mixing`, `js`, and `css` subdirectories.
2. Open `config.py` in directory where you found `serve.py`.  Add the full path name you made note of to the list assigned to `appDirs`.  By default the assignment is <br> `appDirs = []`
3. Restart your server.
4.  Now `localhost/aboutdemo` will get you started.

Note that you cannot access this server from other computers without changing the `localServe` parameter in `config.py`.

The demonstration app together with its code and comments will be enough for some of you to start building your own applications.  Others may want to buy this ebooklet.  It is available in Kindle format from Amazon and in epub format from many other sources.

![*A Simple Programmable Web Server for Python*](http://www.jazimmer.net/reading.jpg)


