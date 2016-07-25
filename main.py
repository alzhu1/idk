import webapp2
from google.appengine.ext import ndb

class Search(ndb.Model):
    location1 = ndb.StringProperty()
    keyword = ndb.StringProperty()

class Result(ndb.Model):
    eventname = ndb.StringProperty()
    location2 = ndb.StringProperty()
    time = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
