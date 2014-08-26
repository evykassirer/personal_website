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
import hashlib
import hmac
SECRET = "ASDH78iuAHSF087iuafkjNAsfs987dgfiuHJ"

"""TO DO:
history
store user that made/edited page
keep track of which is most recent to make a homepage
only make new page when content changes (or new page)
"""

#hashing
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))
def check_secure_val(h):
    val = h.split('|')[0]
    if h==make_secure_val(val):
        return val  

def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))
def make_pw_hash(name, pw, salt=""):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)
#example:
#h = make_pw_hash('spez', 'hunter2')
#print valid_pw('spez', 'hunter2', h) ---- should return true

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
                              
"""def get_posts(update=False):
    key = 'wikiPosts'
    c = memcache.get(key)
    if c is None or update:
        posts = db.GqlQuery("SELECT * FROM WikiPost ORDER BY created DESC")
        posts = list(posts) 
        #this makes it a list so we're not doing the query every time we iterate
        last_queued = datetime.datetime.now()
        c = (posts, last_queued)
        memcache.set(key, c)
    return c"""

def get_post(post_name, update=False):
    key = post_name
    post = memcache.get(key)
    if post is None or update:
        post = db.GqlQuery("SELECT * FROM WikiPost WHERE title = :1 ORDER BY last_edited DESC LIMIT 1", post_name).get()
        #last_queued = datetime.datetime.now()
        if post:
            post = post.as_dict()
            memcache.set(key, post)
            return post
        else: return None
    else: return post
    
class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def check_user(self):
        user_cookie_str = self.request.cookies.get('wikiuser')
        if user_cookie_str:
            return check_secure_val(user_cookie_str)
        else: return False             
      
class WikiPost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    last_edited = db.DateTimeProperty(auto_now_add = True)
    
    def as_dict(self):
        time_fmt = '%c'
        dict = {}
        dict["title"] = str(self.title)
        dict["content"] = str(self.content)
        dict["last_edited"] = self.last_edited.strftime(time_fmt)
        return dict
               
class WikiFront(BaseHandler):
    def get(self):
        user = self.check_user()
        self.render("udacity/wikimain.html", user=user)     

class WikiPostPage(BaseHandler):
    def render_post(self, user=False, title="", content="", last_edited="", error=""):
        self.render("udacity/wikipost.html", user=user, title=title, content=content, last_edited=last_edited, error=error)           
    def get(self, post_name):
        user = self.check_user() 
        post = get_post(str(post_name))
        if post:
            if self.request.url.endswith('.json'):
                self.render_json(post)
            else:
                user = self.check_user()
                self.render_post(user = user, title=post_name, content=post["content"], last_edited=post["last_edited"])
        else:
             self.redirect("/wiki/_edit/"+post_name)

class WikiEditPost(BaseHandler):
    def render_post(self, title="", content="", last_edited="", error="", user=False):
        self.render("udacity/wikiedit.html", title=title, content=content, last_edited=last_edited, error=error, user=user)
    def get(self, post_name):
        user = self.check_user() 
        if not user: self.redirect("/wiki/login")
        post = get_post(str(post_name))                 
        if post:
            self.render_post(title=post_name, content=post["content"], last_edited=post["last_edited"], user=user)    
        else:
            title = post_name
            self.render("udacity/wikiedit.html", title=title, user=user)
    def post(self, post_name):
        title = post_name
        content = self.request.get("content")
        if title and content:
            p = WikiPost(title=title, content=content)
            p.put() #puts in database
            time.sleep(0.3)
            get_post(post_name, True)
            self.redirect("/wiki/" + title)
        else:
            error = "Please enter content for your post!"
            self.render_post(title=title, content=content, error=error)

"""class flushHandler(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect("/blog")"""