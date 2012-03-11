import string, urllib

class FoursquareConfigHandler:
    """This is a mixin class which has several convenience methods for 
    constructing foursquare-related URL, based on the assumption that 
    a configParser instance is in the app configuration."""

    # This memoization stuff might be more elaborate than it's worth
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