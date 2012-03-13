import urllib
import webapp2

class ConfigAware:
    """Classes which inherit from this class will gain the cfg() method, which 
    gets config values out of the config.ini file which is deployed with the 
    application."""
    
    _memo_dict = {}
    
    def __init__(self): pass
    
    # This memoization stuff is almost certainly more elaborate than it's worth.
    # I haven't even thought it out from a class / instance perspective.
    # Plus it could be abstracted.  But for now I'm leaving it in.
    def _poke(self, name, group, value):
        ConfigAware._memo_dict[group + '.' + name] = value
        return value
    
    def _peek(self, group, name):
        return ConfigAware._memo_dict.get(group + '.' + name)
    
    def cfg(self, settingName, settingGroup=None):
        """Return a safely-encoded setting from the given section of the config"""
        if settingGroup is None:
            if not hasattr(self, 'DEFAULT_SETTING_GROUP'):
                raise NotImplementedError('DEFAULT_SETTING_GROUP must be defined')
            settingGroup = self.DEFAULT_SETTING_GROUP
        
        # Check the cache
        if self._peek(settingName, settingGroup) is not None: 
            return self._peek(settingName, settingGroup)
        
        app = webapp2.get_app()
        rawSetting = app.config.get('deployedConfigFile')
        # XXX not certain we always need this
        safeSetting = urllib.quote(rawSetting.get(settingGroup, settingName))
        
        return self._poke(settingName, settingGroup, safeSetting)
