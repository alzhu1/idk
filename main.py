import webapp2
from google.appengine.ext import ndb
import jinja2
import os
from google.appengine.api import urlfetch
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import logging

auth = Oauth1Authenticator(
    consumer_key='LTaCUjkWSPDy9gnmJRLM7g',
    consumer_secret='7pH_DdgonqV6EAqVXdi8Mn934cU',
    token='mSOKE6DC4J2fzx3MF94h0NASZyMWCYY1',
    token_secret='ArwcfHSMGm2taVxzqxx8LF5isCg'
)

client = Client(auth)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


API_KEY = 'LTaCUjkWSPDy9gnmJRLM7g'
API_QUERY = 'https://api.yelp.com/v2/search/'


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
    info = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        keywords = self.request.get('keywords')
        location = self.request.get('location')
        params = {
            'term': 'food '+keywords,
            'lang': 'en'
        }
        request = client.search(location, **params)
        template_vals = {
            'keywords': keywords,
            'location': location,
            'request': request
        }
        logging.info(dir(request.businesses[0])) #REMOVE LATER
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

    def post(self):
        eventname = self.request.get('eventname')
        location = self.request.get('location')
        info = self.request.get('info')

        upload = Upload(eventname=eventname, location=location, time=time, info=info)
        upload.put()

        self.redirect('/nope')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/specifics', SpecificsHandler),
    ('/nope', NopeHandler)
], debug=True)
