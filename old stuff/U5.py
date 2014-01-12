import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom
import json

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
class U5Handler(BaseHandler):
    def get(self):
        url = self.request.get("url")
        if not url: url = "http://eawkassirer.appspot.com/blog/.json"
        c = urllib2.urlopen(url).read()
        #x = minidom.parseString(c)
        #self.write(x)
        
        #j = {"blah":["one", 2, 'th"r"ee']}
        #d = json.dumps(j)
        #self.write(d)
        
        #self.response.out.write(len(x.getElementsByTagName("item")))