#! /usr/local/bin/python

"""Main application file.  This contains the route definitions and whatnot."""

# TODO: I'd like to move most of the 

import pprint
from ConfigParser import SafeConfigParser
import webapp2

from howyoubeen.Foursquare import FoursquareMixin
from howyoubeen.LastFm import LastFmMixin
from howyoubeen.Handlers import JadeHandler, JsonHandler, RedirectHandler
from howyoubeen import Inspiration


class HomePage(JadeHandler):
    def get(self):
        self.render_response('index.jade')

class PlaylistHandler(JadeHandler, FoursquareMixin):
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

class InspirationHandler(JsonHandler, FoursquareMixin):
    # JSON version of above
    def get(self):
        oauth = self.request.GET['oauth']
        checkins = self.getFoursquareCheckins(oauth)
        
        # This feels brittle
        items = checkins['response']['checkins']['items']
        
        inspiration = Inspiration.find(items)
        
        self.render_response([i.to_dict() for i in inspiration])

class OldFoursquareRedirector(JadeHandler, FoursquareMixin):
    # Per https://developer.foursquare.com/overview/auth.html
    def post(self):
        url = self.foursquareRedirectUrl()
        self.response.location = url
        
        if self.app.debug:
            self.response.write('Redirect: <a href="' + url + '">' + url + '</a>')
        else:
            self.response.status = 302
    
    # Purely for debugging
    def get(self): 
        if self.app.debug: 
            return self.post()
        else:
            self.response.status = 404

class FoursquareRedirector(RedirectHandler, FoursquareMixin):
    pass

class LastFmRedirector(RedirectHandler, LastFmMixin):
    pass

class LastFmCallback(JadeHandler, LastFmMixin):
    """last.fm returns the user here after a successful auth"""
    def get(self):
        # XXX handle an error here - foursquare will redir to callback?error=foo
        token = self.request.GET['token']
        sessionKey = self.getLastFmSessionKey(token)
        
        self.response.set_cookie('lastfm.sessionkey', sessionKey,
                comment='last.fm web service session key')
        
        self.response.location = '/'
        #self.response.status = 302

class FoursquareCallback(JadeHandler, FoursquareMixin):
    """Once a user accepts authentication on foursquare, they're sent back here with a 
    code parameter on the query string.  We then need to request an access token from 
    foursquare, which will be returned to us in a JSON response body.  
    
    Once we get the token, we save it as a session cookie and then redirect the user
    to the home page (hoping the classic cookie/redirect issues don't come into play 
    here)."""
    def get(self):
        # XXX handle an error here - foursquare will redir to callback?error=foo
        code = self.request.GET['code']
        url = self.foursquareAccessTokenUrl(code)
        accessCode = self.getFoursquareAccessToken(code)
        
        self.response.set_cookie('foursquare.oauth', accessCode,
                comment='Foursquare session authentication token')
        #self.response.location = '/playlist?oauth=' + urllib.quote(accessCode)
        self.response.location = '/'
        self.response.status = 302

deployedConfigFile = SafeConfigParser()
deployedConfigFile.read('config/config.ini')

app = webapp2.WSGIApplication(routes=[
         ('/', HomePage),
         ('/foursquare-redirect',   FoursquareRedirector),
         ('/foursquare-callback',   FoursquareCallback),
         ('/lastfm-redirect',       LastFmRedirector),
         ('/lastfm-callback',       LastFmCallback),
         ('/playlist',              PlaylistHandler),
         ('/inspiration.json',      InspirationHandler)
        ], 
        config={'deployedConfigFile': deployedConfigFile},
        debug=deployedConfigFile.getboolean('general', 'debug'))
