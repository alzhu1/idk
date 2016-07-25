import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

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
