import logging, pprint, hashlib, urllib, urllib2
from webapp2_extras import json
from lxml import etree
#import pylast

import Handlers, Config

# Routines for dealing with the last.fm API.
# cf http://www.last.fm/api/

# Note, chunks of this code are based on pyLast, which 
# seems like a good library, but apart from the authentication 
# bit I'm doing all the last.fm interaction at the client level.
# http://code.google.com/p/pylast/

# A few constants
USER_AGENT = 'how-you-been/1.0'
LAST_FM_ROOT = 'http://ws.audioscrobbler.com/2.0/'

class LastFmMixin(Handlers.WebAuth, Config.ConfigAware): 
    """Construct the URL we use to auth users at last.fm"""
    
    # Default setting for config lookups
    DEFAULT_SETTING_GROUP = 'last.fm'
    
    # Name of the session cookie we store data in
    SESSIONKEY_COOKIE = 'lastfm.sessionKey'
    USERNAME_COOKIE = 'lastfm.username'
    
    def getAuthRedirectUrl(self):
        host = self.request.environ['HTTP_HOST']
        url = ('http://www.last.fm/api/auth/' +
               '?api_key=' + self.cfg('api_key') +
               '&cb=http://' + host + '/lastfm-callback')
        return url
    
    def _lastFmApiUrl(self, url): pass
    
    def getLastFmSessionKey(self, token):
        """Given an access code, make a call to last.fm. Find the user's name and a session key,
        and save both values into cookies."""
        
        apiRequest = LastFmApiRequest('auth.getSession', {'token': unicode(token).encode('utf-8')})
        
        logging.debug('sessionKey URL: ' + apiRequest.url())
        
        response = apiRequest.execute()
        root = response.getroot()
        
        sessionKey = root.xpath('//key/text()')[0]
        username = root.xpath('//name/text()')[0]
        
        logging.debug('user:' + username + ' session:' + sessionKey)
        
        # I'm not crazy about the way this couples the mixin and webapp2.RequestHandler
        self.setCookie(self.SESSIONKEY_COOKIE, sessionKey)
        self.setCookie(self.USERNAME_COOKIE, username)

class LastFmApiRequest(Config.ConfigAware):
    """Stripped-down pylast._Request class usable for authentication"""
    DEFAULT_SETTING_GROUP = 'last.fm'
    def __init__(self, method, params={}):
        Config.ConfigAware.__init__(self)
        self.params = params
        
        self.params['api_key'] = self.cfg('api_key')
        self.params['method'] = method
        
        # Generate signature
        self.params['api_sig'] = self.signature(self.params)
    
    def signature(self, params):
        """Returns a 32-character hexadecimal md5 hash of the signature string."""
        string = ''.join(key + params[key] for key in sorted(params.keys()))
        return md5(string + self.cfg('secret'))
    
    def url(self):
        """Get the URL for this method"""
        queries = ['='.join([key, urllib.quote_plus(self.params[key])]) for key in self.params]
        s = LAST_FM_ROOT + '?' + '&'.join(queries)
        return s
    
    def execute(self):
        """Fetch the method from last.fm; return the result"""
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept-Charset': 'utf-8',
            'User-Agent': USER_AGENT
        }
        request = urllib2.Request(self.url(), headers=headers)
        response = urllib2.urlopen(request)
        
        return etree.parse(response)
    
    def __repr__(self): return repr(self.params)

def md5(text):
        h = hashlib.md5()
        h.update(unicode(text).encode("utf-8"))

        return h.hexdigest()
