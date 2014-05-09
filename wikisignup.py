import os
import webapp2
import jinja2
import re
import random
import string
import hashlib
import hmac
from google.appengine.ext import db
SECRET = "ASDH78iuAHSF087iuafkjNAsfs987dgfiuHJ"


#jinja templates    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#database creation
class WikiUser(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required = False)
    
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())
    @classmethod
    def by_name(cls, uid):
        return User.all().filter('name = ', name).get()

#regular expressions to match for correct input
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
def new_username(username):
    user = db.GqlQuery("select * from WikiUser where username = :1", username).get()
    if user: return False
    else: return True
def valid_pass(password):
    return PASS_RE.match(password) 
def same_pass(password, verify):
    return password == verify
def valid_email(email):
    return email == "" or EMAIL_RE.match(email)    
    
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
        
class WikiSignUpHandler(BaseHandler):
    def get(self):
        next_url = self.request.headers.get('referer', '/wiki')
        user_cookie_str = self.request.cookies.get('wikiuser')
        if user_cookie_str:
            cookie_val = check_secure_val(user_cookie_str)
            if cookie_val:
                self.redirect("/wiki")
            else: self.render('signup.html', next_url=next_url)
        else: self.render('signup.html', next_url=next_url)
    def post(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        next_url = str(self.request.get('next_url'))
        if not next_url or '/login' in next_url:
            next_url = '/wiki'
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        template_values = {'username':username, 'email':email}
        error = False
        if(not valid_username(username)):
            template_values['usererror'] = "That's not a valid username"
            error = True
        else:
            if(not new_username(username)):
                template_values['newusererror'] = "That user already exists"
                error = True
        if(not valid_pass(password)):
            template_values['passerror'] = "That wasn't a valid password."
            error = True            
        else: 
            if(not same_pass(password, verify)):
                template_values['verifyerror'] = "Your passwords didn't match."
                error = True
        if(not valid_email(email)):
            template_values['emailerror'] = "That's not a valid email."
            error = True
        if(error): 
            self.render('signup.html', **template_values)
        else: 
            if email:
                u = WikiUser(username=username, password=make_pw_hash(username, password), email=email)
            else:
                u = WikiUser(username=username, password=make_pw_hash(username, password))
            u.put() #puts in database
            self.response.headers.add_header('Set-Cookie', 'wikiuser=%s; Path=/' %str(make_secure_val(username)))
            self.redirect(next_url)