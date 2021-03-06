import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from google.appengine.api import urlfetch
import logging
import json
from datetime import datetime
from datetime import timedelta

auth = Oauth1Authenticator(
    consumer_key='LTaCUjkWSPDy9gnmJRLM7g',
    consumer_secret='7pH_DdgonqV6EAqVXdi8Mn934cU',
    token='mSOKE6DC4J2fzx3MF94h0NASZyMWCYY1',
    token_secret='ArwcfHSMGm2taVxzqxx8LF5isCg'
)

client = Client(auth)
EVENTBRITE_TOKEN = '6V7MG6DMIX6P4FWU5GJW'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
#urlfetch.set_default_fetch_deadline(60)


class Search(ndb.Model):
    location = ndb.StringProperty()
    keyword = ndb.StringProperty()

class Results(ndb.Model):
    eventname = ndb.StringProperty()
    location = ndb.StringProperty()

class Upload(ndb.Model):
    eventname = ndb.StringProperty()
    location = ndb.StringProperty()
    info = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

    def post(self):
        eventname = self.request.get('eventname')
        location = self.request.get('location')
        info = self.request.get('info')

        upload = Upload(eventname=eventname, location=location, info=info)
        upload.put()

        self.redirect('/')

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        keywords = self.request.get('keywords')
        location = self.request.get('location')
        page = self.request.get('page')
        locount = 0
        keycount = 0

        if page == '':
            page=0
        else:
            page=int(page)

        for ch in range(len(location)):
            if location[ch] == ' ':
                locount = locount + 1
        for ch in range(len(keywords)):
            if keywords[ch] == ' ':
                keycount = keycount + 1
        location = location.replace(' ', '+', locount)
        keywords = keywords.replace(' ', '+', keycount)

        food_params = {
            'term': keywords,
            'lang': 'en',
            'category_filter': 'restaurants',
            'radius_filter': 3219,
            'sort': 2,
            'offset': 0+page*10,
            'limit': 10
        }
        event_params = {
            'term': keywords,
            'lang': 'en',
            'category_filter': 'active,arts', #maybe shopping?
            'radius_filter': 3219,
            'sort': 2,
            'offset': 0+page*10,
            'limit': 10
        }
        EVENTBRITE_URL = 'https://www.eventbriteapi.com/v3/events/search/?token={}&location.address={}&location.within=2mi&page={}'.format(EVENTBRITE_TOKEN,location,1+int(page/5)) #figure out how to incorporate page number
        eventbrite_response = urlfetch.fetch(EVENTBRITE_URL)
        events = json.loads(eventbrite_response.content)

        foods = client.search(location, **food_params) #dropdown menu or search?
        yelp_events = client.search(location, **event_params)

        template_vals = {
            'foods': foods,
            'yelp_events': yelp_events,
            'events': events,
            'keywords':keywords,
            'location':location,
            'page':page
        }
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render(template_vals))


class NopeHandler(webapp2.RequestHandler):
    def get(self):
        events = Upload.query().order(-Upload.date).fetch()
        template_values = {'events': events}
        for event in events:
            if (datetime.now() - event.date).days >= 7:
                event.key.delete()


        template = jinja_environment.get_template('nope.html')
        self.response.write(template.render(template_values))

    def post(self):
        eventname = self.request.get('eventname')
        location = self.request.get('location')
        info = self.request.get('info')

        upload = Upload(eventname=eventname, location=location, info=info, date=datetime.now())
        upload.put()

        self.redirect('/nope')

class SubmitIdeaHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('submitIdea.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/nope', NopeHandler),
    ('/submitIdea', SubmitIdeaHandler),
    ('/about', AboutHandler)
], debug=True)
