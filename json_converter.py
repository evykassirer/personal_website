import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom
import json
from google.appengine.ext import db
    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

def get_dict(post):
    dict = {}
    dict["subject"] = str(post.body)
    dict["content"] = str(post.body)
    dict["created"] = post.created.strftime("%b %d, %Y")
    dict["last_modified"] = post.last_modified.strftime("%b %d, %Y")
    return dict
      
class JsonPostPage(BaseHandler):
    def get(self, post_id):
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        post = Post.get_by_id(int(post_id)) 
        if not post:
            self.redirect("blog/404error")
            return       
        self.write(json.dumps(get_dict(post)))
        
class JsonBlogFront(BaseHandler):
    def get(self):
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        lst = []
        for p in posts:
            lst.append(get_dict(p))
        self.write(json.dumps(lst))