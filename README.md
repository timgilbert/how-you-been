whence
------

This is a simple GAE application written in python.  The aim is to make a 
sort of last.fm / foursquare mashup.  I hope to use [Google's webapp2][webapp2] 
along with [pyjade][pyjade] through [jinja2][jinja2], since I've come to 
enjoy writing jade.

Installing
----------

I've tried to set up the environment for this project as in 
[this Stack Overflow answer][answer].  After checking out the code, cd into 
its root directory and run:

    virtualenv -p /usr/local/bin/python --no-site-packages --distribute .
    pip install pyjade
    ln -s lib/python2.7/site-packages/pyjade src/
    

[webapp2]: http://webapp-improved.appspot.com/index.html
[jinja2]: http://webapp-improved.appspot.com/api/webapp2_extras/jinja2.html
[pyjade]: https://github.com/syrusakbary/pyjade
[answer]: http://stackoverflow.com/a/4863970/87990
