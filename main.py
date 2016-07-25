import webapp2
from google.appengine.ext import ndb
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class Search(ndb.Model):
    location1 = ndb.StringProperty()
    keyword = ndb.StringProperty()

class Results(ndb.Model):
    eventname = ndb.StringProperty()
    location2 = ndb.StringProperty()
    time = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render())
        self.response.write('These are the results')

class SpecificsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('specifics.html')
        self.response.write(template.render())
        self.response.write('These are the specifics')

class NopeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('nope.html')
        self.response.write(template.render())
        self.response.write('You think of something')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/specifics', SpecificsHandler),
    ('/nope', NopeHandler)
], debug=True)
