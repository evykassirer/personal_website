import os
import webapp2
import jinja2
import random
import string
import hmac
import hashlib
from signup import User
from google.appengine.ext import db
SECRET = "ASDH78iuAHSF087iuafkjNAsfs987dgfiuHJ"


#jinja templates    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

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
    
    
class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
class WikiLogInHandler(BaseHandler):
    def get(self):
        next_url = self.request.headers.get('referer', '/wiki')
        user_cookie_str = self.request.cookies.get('wikiuser')
        if user_cookie_str:
            cookie_val = check_secure_val(user_cookie_str)
            if cookie_val:
                self.redirect("/wiki")
            else: 
                self.response.headers.add_header('Set-Cookie', 'wikiuser=%s; Path=/' %"")
                self.render('login.html', next_url = next_url)
        else: self.render('login.html', next_url = next_url)
    def post(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        next_url = str(self.request.get('next_url'))
        if not next_url or '/login' in next_url:
            next_url = '/wiki'
        
        username = self.request.get('username')
        password = self.request.get('password')
        user = db.GqlQuery("select * from WikiUser where username = :1", username).get()
        error = False
        if(not user): error = True
        elif(not valid_pw(username, password, user.password)): error = True
        if(error): 
            self.render('login.html', error="Invalid login")
        else: 
            self.response.headers.add_header('Set-Cookie', 'wikiuser=%s; Path=/' %str(make_secure_val(username)))
            self.redirect(next_url)

class WikiLogOutHandler(BaseHandler):
    def get(self):
        next_url = self.request.headers.get('referer', '/wiki')
        self.response.headers.add_header('Set-Cookie', 'wikiuser=%s; Path=/' %"")
        self.redirect(next_url)
