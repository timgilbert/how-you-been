import string, urllib, urllib2
from webapp2_extras import json

class FoursquareException(Exception):
    def __init__(self, value): self.value = value
    def __str__(self): return repr(self.value)

class FoursquareConfigHandler:
    """This is a mixin class which has several convenience methods for 
    constructing foursquare-related URL, based on the assumption that 
    a configParser instance is in the app configuration."""

    # This memoization stuff is almost certainly more elaborate than it's worth
    # I haven't even thought through it from a class / instance perspective
    # Plus it could be abstracted.  Oh well.
    def _poke(self, name, value):
        if not hasattr(self, '_memo_dict'): 
            self._memo_dict = {}
        self._memo_dict[name] = value
        return value
    
    def _peek(self, name):
        if not hasattr(self, '_memo_dict'):  return None
        return self._memo_dict.get(name)
    
    def cfg(self, settingName):
        """Return a safely-encoded setting from the foursquare section of the config"""
        if self._peek(settingName) is not None: return self._peek(settingName)
        rawSetting = self.app.config.get('deployedConfigFile')
        
        #print rawSetting.get('foursquare', settingName)
        
        safeSetting = urllib.quote(rawSetting.get('foursquare', settingName))
        return self._poke(settingName, safeSetting)
    
    def foursquareRedirectUrl(self):
        url = ('https://foursquare.com/oauth2/authenticate' +
               '?client_id=' + self.cfg('client_id') +
               '&response_type=code' + 
               '&redirect_uri=' + self.cfg('callback'))
        return url
        
    def foursquareAccessTokenUrl(self, code):
        url = ('https://foursquare.com/oauth2/access_token' +
               '?client_id=' + self.cfg('client_id') +
               '&client_secret=' + self.cfg('client_secret') + 
               '&grant_type=authorization_code' +
               '&redirect_uri=' + self.cfg('callback') + 
               '&code=' + urllib.quote(code))
        return url
    
    def getFoursquareAccessToken(self, code):
        """Given an access code, make an access token to foursquare and return 
        the access token they give us.  Raise an error if they return one."""
        url = self.foursquareAccessTokenUrl(code)
        httpResponse = urllib2.urlopen(url)
        result = json.decode(httpResponse.read())
        
        if 'access_token' in result:
            access_token = str(result['access_token'])
        else:
            raise FoursquareException(result)
            
        return access_token