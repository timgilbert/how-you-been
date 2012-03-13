import logging, traceback

import webapp2
from webapp2_extras import jinja2, json

import Inspiration

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
        
class JsonHandler(BaseHandler):
    """Base class for returning an object as pure json"""
    # XXX should have some kind of error handler here, too
    def render_response(self, item, **context):
        indent = 1 if self.app.debug else 0
        
        self.response.content_type = "application/json"
        content = json.encode(item, encoding='utf-8', ensure_ascii=False, indent=indent, **context)
        self.response.write(content)

class WebAuth:
    """Abstract base class which is used by web auth routines"""
    def getAuthRedirectUrl(self):
        raise NotImplementedError('Subclasses must override this abstract method')
    
    def setCookie(self, name, value):
        """Set an authorization-related cookie in the response."""
        self.response.set_cookie(name, value)

class RedirectHandler(JadeHandler):
    """Handler which gets a redirection URL from a mixin and then redrects to it."""
    def post(self):
        
        if not hasattr(self, 'getAuthRedirectUrl'):
            raise NotImplementedError('Subclasses of RedirectHandler must mix in a subclass of WebAuth')
        
        url = self.getAuthRedirectUrl()
        self.response.location = url

        if self.app.debug and True:
            # This is a little annoying, commenting it out for now
            self.response.write('Redirect: <a href="' + url + '">' + url + '</a>')
        else:
            self.response.status = 302

    # Purely for debugging
    def get(self): 
        if self.app.debug: 
            return self.post()
        else:
            self.response.status = 404
    