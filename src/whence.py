import os, string
from ConfigParser import SafeConfigParser
import webapp2
from webapp2_extras import jinja2

class JadeHandler(webapp2.RequestHandler):
    # Per http://stackoverflow.com/a/7081653/87990
    @staticmethod
    def jade_factory(app):
        j = jinja2.Jinja2(app)
        j.environment.add_extension('pyjade.ext.jinja.PyJadeExtension')
        return j

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app, factory=JadeHandler.jade_factory)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class HomePage(JadeHandler):
    def get(self):
        client_id = self.app.config.get('file').get('foursquare', 'client_id')
        context = {
            'foo': 'Hello, world!',
            'message': client_id
        }
        self.render_response('index.jade', **context)

class FourSquareRedirector(webapp2.RequestHandler):
    # Per https://developer.foursquare.com/overview/auth.html
    def post(self):
        tmpl = string.Template('https://foursquare.com/oauth2/authenticate' +
               '?client_id=${client_id}' +
               '&response_type=code' + 
               '&redirect_uri=${endpoint}')
        url = tmpl.substitute(client_id='sorry_foursquare_dev_testing', endpoint='http://foo')
        self.response.location = url
        #self.response.status = 302
        
        #self.response.content_type = "text/html"
        self.response.write('<a href="' + url + '">' + url + '</a>' )

class FourSquareCallback(webapp2.RequestHandler):
    """Once a user accepts authentication on foursquare, they're sent back here with a 
    code parameter on the query string.  We then need to request an access token from 
    foursquare, which will be returned to us in a JSON response body.
    """
    def get(self):
        pass

configFile = SafeConfigParser()
configFile.read('config.ini')

app = webapp2.WSGIApplication(routes=[
         ('/', HomePage),
         ('/foursquare-redirect', FourSquareRedirector),
         ('/foursquare-callback', FourSquareCallback)
        ], 
        config={'file': configFile},
        debug=True)
