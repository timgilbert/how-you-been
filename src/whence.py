import os, string, logging, traceback, pprint, urllib
from ConfigParser import SafeConfigParser
import webapp2
from webapp2_extras import jinja2, json

import Inspiration
from FoursquareConfig import FoursquareConfigHandler

class BaseHandler(webapp2.RequestHandler):
    def handle_exception(self, exception, debug):
        # Todo: not certain this does more harm than good
        logging.exception(exception)

        context = {'exception': exception, 
                   'traceback':traceback.format_exc(),
                   'debug': debug}

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        http_status = 500
        if isinstance(exception, webapp2.HTTPException):
            http_status = exception.code
        
        self.response.set_status(http_status)
        context['http_status'] = http_status
        
        self.render_response('error.jade', **context)

class JadeHandler(BaseHandler):
    # Per http://stackoverflow.com/a/7081653/87990
    """Base class which passes contexts to pyjade templates for rendering"""
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
        
class JsonHandler(webapp2.RequestHandler):
    """Base class for returning an object as pure json"""
    # XXX should have some kind of error handler here, too
    def render_response(self, item, **context):
        indent = 1 if self.app.debug else 0
        
        self.response.content_type = "application/json"
        content = json.encode(item, encoding='utf-8', ensure_ascii=False, indent=indent, **context)
        self.response.write(content)
        

class HomePage(JadeHandler, FoursquareConfigHandler):
    def get(self):
        self.render_response('index.jade')

class PlaylistHandler(JadeHandler, FoursquareConfigHandler):
    def get(self):
        oauth = self.request.GET['oauth']
        checkins = self.getFoursquareCheckins(oauth)
        
        # This feels brittle
        items = checkins['response']['checkins']['items']
        
        inspiration = Inspiration.find(items)
        
        context = {
            'oauth':    oauth,
            'pretty':   pprint.pformat(items, 1, 120),
            'inspiration':   pprint.pformat(inspiration, 1, 120),
            'encoding':   checkins['encoding'],
            'debug':    self.app.debug
        }
        self.render_response('playlist.jade', **context)

class InspirationHandler(JsonHandler, FoursquareConfigHandler):
    # JSON version of above
    def get(self):
        oauth = self.request.GET['oauth']
        checkins = self.getFoursquareCheckins(oauth)
        
        # This feels brittle
        items = checkins['response']['checkins']['items']
        
        inspiration = Inspiration.find(items)
        
        self.render_response([i.to_dict() for i in inspiration])

class FoursquareRedirector(JadeHandler, FoursquareConfigHandler):
    # Per https://developer.foursquare.com/overview/auth.html
    def post(self):
        url = self.foursquareRedirectUrl()
        self.response.location = url
        #self.response.status = 302
        
        #self.response.content_type = "text/html"
        self.response.write('<a href="' + url + '">' + url + '</a>')
    
    # Purely for debugging
    def get(self): 
        if self.app.debug: 
            return self.post()
        else:
            self.response.status = 404

class FoursquareCallback(JadeHandler, FoursquareConfigHandler):
    """Once a user accepts authentication on foursquare, they're sent back here with a 
    code parameter on the query string.  We then need to request an access token from 
    foursquare, which will be returned to us in a JSON response body.  Once we get the 
    token, we'll redirect the user to another page with the token in the URL."""
    def get(self):
        # XXX handle an error here - foursquare will redir to callback?error=foo
        code = self.request.GET['code']
        url = self.foursquareAccessTokenUrl(code)
        accessCode = self.getFoursquareAccessToken(code)
        
        self.response.location = '/playlist?oauth=' + urllib.quote(accessCode)
        self.response.status = 302

deployedConfigFile = SafeConfigParser()
deployedConfigFile.read('config/config.ini')

app = webapp2.WSGIApplication(routes=[
         ('/', HomePage),
         ('/foursquare-redirect',   FoursquareRedirector),
         ('/foursquare-callback',   FoursquareCallback),
         ('/playlist',              PlaylistHandler),
         ('/inspiration.json',      InspirationHandler)
        ], 
        config={'deployedConfigFile': deployedConfigFile},
        debug=deployedConfigFile.getboolean('general', 'debug'))
