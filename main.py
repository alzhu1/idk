import webapp2
from google.appengine.ext import ndb
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

<<<<<<< HEAD
API_KEY = LTaCUjkWSPDy9gnmJRLM7g
=======
API_QUERY = 'https://api.yelp.com/v2/search/'
>>>>>>> 2bd929c4d910e06cb357bff46bb1b27826851cae

class Search(ndb.Model):
    location = ndb.StringProperty()
    keyword = ndb.StringProperty()

class Results(ndb.Model):
    eventname = ndb.StringProperty()
    location = ndb.StringProperty()
    time = ndb.DateTimeProperty()

class Upload(ndb.Model):
    eventname = ndb.StringProperty()
    location = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    info = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

    def post(self):
        eventname = self.request.get('eventname')
        location = self.request.get('location')
        time = self.request.get('time')
        info = self.request.get('info')

        upload = Upload(eventname=eventname, location=location, time=time, info=info)
        upload.put()

        self.redirect('/nope')

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        keywords = self.request.get('keywords')
        location = self.request.get('location')
        template_vals = {
            'keywords': keywords,
            'location': location
        }
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render(template_vals))

class SpecificsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('specifics.html')
        self.response.write(template.render())

class NopeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('nope.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/specifics', SpecificsHandler),
    ('/nope', NopeHandler)
], debug=True)
