import string, urllib, urllib2, logging
from webapp2_extras import json
import Handlers, Config

class FoursquareException(Exception):
    def __init__(self, message, value): 
        super(self, Exception).__init__(message)
        self.value = value

class FoursquareApiException(FoursquareException): pass

class FoursquareMixin(Handlers.WebAuth, Config.ConfigAware):
    """This is a mixin class which has several convenience methods for 
    constructing foursquare-related URL, based on the assumption that 
    a configParser instance is in the app configuration."""
    
    # Default setting for config lookups
    DEFAULT_SETTING_GROUP = 'foursquare'
    
    # Name of the session cookie we store data in
    COOKIE_NAME = 'foursquare.oauth'
    
    def getAuthRedirectUrl(self):
        """Construct the URL we'll initially use to send users off to foursquare for OAuth"""
        url = ('https://foursquare.com/oauth2/authenticate' +
               '?client_id=' + self.cfg('client_id') +
               '&response_type=code' + 
               '&redirect_uri=' + self.cfg('callback'))
        return url
        
    def foursquareAccessTokenUrl(self, code):
        """Construct a URL to use to get an access token from foursquare's OAuth"""
        url = ('https://foursquare.com/oauth2/access_token' +
               '?client_id=' + self.cfg('client_id') +
               '&client_secret=' + self.cfg('client_secret') + 
               '&grant_type=authorization_code' +
               '&redirect_uri=' + self.cfg('callback') + 
               '&code=' + urllib.quote(code))
        return url
    
    def getFoursquareAccessToken(self, code):
        """Given an access code, make an OAuth call to foursquare and return 
        the access token they give us.  Raise an error if they return one."""
        url = self.foursquareAccessTokenUrl(code)
        httpResponse = urllib2.urlopen(url)
        result = json.decode(httpResponse.read())
        
        if 'access_token' in result:
            access_token = str(result['access_token'])
        else:
            raise FoursquareException(result)
            
        return access_token
    
    def getFoursquareCheckins(self, accessToken):
        """Get the list of the signed-in user's checkins, per 
        https://developer.foursquare.com/docs/users/checkins"""
        return self.getFoursquareApi('users/self/checkins', accessToken)
    
    def foursquareApiUrl(self, apiPath, accessToken):
        """Return a complete URL to the relevant foursquare API endpoint."""
        baseUrl = 'https://api.foursquare.com/v2/' + apiPath # TODO: make this a cfg value
        return baseUrl + '?' + urllib.urlencode({
            'v': self.cfg('apiversion'),
            'oauth_token': accessToken
        })
    
    def getFoursquareApi(self, apiPath, accessToken):
        """Given a partial foursquare API endpoint path and an auth token, 
        make a request to the endpoint, parse the result, and return it."""
        url = self.foursquareApiUrl(apiPath, accessToken)
        request = urllib2.urlopen(url)
        content = request.read()
        
        # Criminy. http://stackoverflow.com/a/1020931/87990
        encoding = request.headers['content-type'].split('charset=')[-1]
        ucontent = unicode(content, encoding)
        jsonResult = json.decode(ucontent)
        jsonResult['encoding'] = encoding
        return self._checkForApiErrors(jsonResult)
    
    def _checkForApiErrors(self, jsonResult):
        """Inspect a parsed json response for any errors as described here:
        https://developer.foursquare.com/overview/responses; if any exist, 
        raise an error."""
        if 'meta' not in jsonResult:
            raise FoursquareApiException('API result is missing "meta" member', jsonResult)
        
        return jsonResult