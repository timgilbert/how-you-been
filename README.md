How You Been?
-------------

This is a simple [Google App Engine][gae] application written in python.  The aim 
is to make foursquare / last.fm mashup which looks at your foursquare history and 
then generates a playlist of songs related to the places you've been recently.  

It's using [Google's webapp2][webapp2] along with [pyjade][pyjade] through 
[jinja2][jinja2], since I've come to enjoy writing jade.  I'm using 
[clifff's fork][fork] of the [javascript-last.fm-api project][js-last] 
since it has important bug fixes that haven't been merged yet.


A working installation of this application should eventually be up and running at 
[http://how-you-been.appspot.com/][appspot].

Installing
----------

I've tried to set up the environment for this project as in 
[this Stack Overflow answer][answer].  After checking out the code, cd into 
its root directory and run:

    virtualenv -p /usr/local/bin/python --no-site-packages --distribute .
    pip install pyjade
    pip install lxml
    cd src
    ln -s ../lib/python2.7/site-packages/pyjade .
    ln -s ../lib/python2.7/site-packages/lxml .
    dev_appserver.py .

[gae]:      http://code.google.com/appengine
[webapp2]:  http://webapp-improved.appspot.com/index.html
[jinja2]:   http://webapp-improved.appspot.com/api/webapp2_extras/jinja2.html
[pyjade]:   https://github.com/syrusakbary/pyjade
[answer]:   http://stackoverflow.com/a/4863970/87990
[appspot]:  http://how-you-been.appspot.com/
[fork]:     https://github.com/clifff/javascript-last.fm-api
[js-last]:  https://github.com/fxb/javascript-last.fm-api
