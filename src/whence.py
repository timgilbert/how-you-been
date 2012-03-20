#! /usr/local/bin/python

"""Main application file.  This contains the route definitions and whatnot."""

# TODO: 
# The thinner this file is, the happier I'll feel.  Ideally it should just be routing
#   and app setup.
# The last.fm session key is forever, we should probably give it a year or so timeout
#   http://www.last.fm/group/Last.fm+Web+Services/forum/21604/_/2031013
# Same with foursquare's oauth token (for now)
#   https://developer.foursquare.com/overview/auth

import pprint
from ConfigParser import SafeConfigParser
import webapp2

from howyoubeen.Foursquare import FoursquareMixin
from howyoubeen.LastFm import LastFmMixin
from howyoubeen.Handlers import JadeHandler, JsonHandler, RedirectHandler
from howyoubeen import Inspiration


class HomePage(JadeHandler):
    def get(self): self.render_response('index.jade')

class AboutPage(JadeHandler):
    def get(self): self.render_response('about.jade')

class GammaPage(JadeHandler):
    def get(self): self.render_response('gamma.jade')

class TestPage(JadeHandler):
    def get(self):
        if self.app.debug:
            self.render_response('test.jade')
        else:
            self.redirect('/')

class PlaylistHandler(JadeHandler, FoursquareMixin):
    def get(self):
        
        if FoursquareMixin.OAUTH_COOKIE not in self.request.cookies:
            logging.debug('No cookie found at playlist, redirecting to homepage')
            self.redirect('/')
            return
        
        oauth = self.request.cookies[FoursquareMixin.OAUTH_COOKIE]
        checkins = self.getFoursquareCheckins(oauth)
        
        # This feels brittle
        items = checkins['response']['checkins']['items']
        
        inspiration = Inspiration.find(items)
        
        context = {
            'oauth':    oauth,
            'lastFmApiKey': self.cfg('api_key', section='last.fm'),
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

class FoursquareRedirector(RedirectHandler, FoursquareMixin):
    pass

class LastFmRedirector(RedirectHandler, LastFmMixin):
    pass

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
        
        self.redirect('/')

class LastFmCallback(JadeHandler, LastFmMixin):
    """last.fm returns the user here after a successful auth.  We contact them to get a
    session key and a username, and then redirect.
    """
    def get(self):
        # XXX handle errors, and maybe generalize
        token = self.request.GET['token']
        sessionKey = self.getLastFmSessionKey(token)

        self.redirect('/')

deployedConfigFile = SafeConfigParser()
deployedConfigFile.read('config/config.ini')

app = webapp2.WSGIApplication(routes=[
         ('/',                      GammaPage),
         ('/home',                  HomePage),
         ('/about',                 AboutPage),
         ('/test',                  TestPage),
         ('/foursquare-redirect',   FoursquareRedirector),
         ('/foursquare-callback',   FoursquareCallback),
         ('/lastfm-redirect',       LastFmRedirector),
         ('/lastfm-callback',       LastFmCallback),
         ('/playlist',              PlaylistHandler),
         ('/inspiration.json',      InspirationHandler)
        ], 
        config={'deployedConfigFile': deployedConfigFile},
        debug=deployedConfigFile.getboolean('general', 'debug'))
