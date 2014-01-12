import os
import webapp2
import jinja2
import urllib2
import time
import datetime
from xml.dom import minidom
import json
from google.appengine.api import memcache
from google.appengine.ext import db
    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def get_dict(post):
    dict = {}
    dict["subject"] = str(post.body)
    dict["content"] = str(post.body)
    dict["created"] = post.created.strftime("%b %d, %Y")
    dict["last_modified"] = post.last_modified.strftime("%b %d, %Y")
    return dict
    
def get_posts(update=False):
    key = 'posts'
    c = memcache.get(key)
    if c is None or update:
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        posts = list(posts) 
        #this makes it a list so we're not doing the query every time we iterate
        last_queued = datetime.datetime.now()
        c = (posts, last_queued)
        memcache.set(key, c)
    return c

def get_post(id):
    key = id
    c = memcache.get(key)
    if c is None:
        post = Post.get_by_id(int(id)) 
        last_queued = datetime.datetime.now()
        c = (post, last_queued)
        memcache.set(key, c)
    return c
    
class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_json(self, d):
        json_text = json.dumps(d)
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        self.write(json_text)
      
class Post(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def as_dict(self):
        time_fmt = '%c'
        dict = {}
        dict["subject"] = str(self.body)
        dict["content"] = str(self.body)
        dict["created"] = self.created.strftime(time_fmt)
        dict["last_modified"] = self.last_modified.strftime(time_fmt)
        return dict
               
class BlogFront(BaseHandler):
    def render_front(self):
        (posts, last_queued) = get_posts()
        time_since=(datetime.datetime.now()-last_queued).total_seconds()
        s = "Queried %s seconds ago" % time_since
        if time_since == 1:
            s = s.replace("seconds", "second")
        self.render("front.html", posts=posts, s=s)
    def get(self):
        if self.request.url.endswith('.json'):
            posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
            lst = []
            for p in posts:
                lst.append(p.as_dict())
            self.render_json(lst)
        else: self.render_front()        

class PostPage(BaseHandler):
    def get(self, post_id):
        (post, last_queued) = get_post((str(post_id))) 
        if not post:
            self.redirect("blog/404error")
            return
        if self.request.url.endswith('.json'):
            self.render_json(post.as_dict())
        else: 
            time_since=(datetime.datetime.now()-last_queued).total_seconds()
            s = "Queried %s seconds ago" % time_since
            if time_since == 1:
                s = s.replace("seconds", "second")
            self.render("singlepost.html", post=post, s=s)
        
class NewPost(BaseHandler):
    def render_newpost(self, title="", body="", error=""):
        self.render("newblogentry.html", title=title, body=body, error=error)
    def get(self):
       self.render_newpost()        
    def post(self):
        title = self.request.get("subject")
        body = self.request.get("content")
        if title and body:
            p = Post(title=title, body=body)
            p.put() #puts in database
            id = p.key().id()
            time.sleep(0.1)
            get_posts(True)
            self.redirect("/blog/post/" + str(id))
        else:
            error = "Please enter both a title and a body for your blog post!"
            self.render_newpost(title, body, error)

class error404handler(BaseHandler):
    def get(self):
        self.render("404Error.html")

class flushHandler(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect("/blog")