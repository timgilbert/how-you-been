import string

class FoursquareConfigHandler:
    """This is a mixin class which has several convenience methods for 
    constructing foursquare-related URL, based on the assumption that 
    a configParser instance is in the app configuration."""
    
    def cfg(self, settingName):
        return self.app.config.get('deployedConfigFile').get('foursquare', settingName)
    
    def foursquareRedirectUrl(self):
        tmpl = string.Template('https://foursquare.com/oauth2/authenticate' +
                   '?client_id=${client_id}' +
                   '&response_type=code' + 
                   '&redirect_uri=${callback}')
               
        return tmpl.substitute(client_id=self.cfg('client_id'),
                               callback=self.cfg('callback'))
        
