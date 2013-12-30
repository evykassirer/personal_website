import os
import webapp2
import jinja2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
def valid_pass(password):
    return PASS_RE.match(password) 
def same_pass(password, verify):
    return password == verify
def valid_email(email):
    return email == "" or EMAIL_RE.match(email)
    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

                              
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
class SignUpHandler(BaseHandler):
    def get(self):
        self.render('signup.html')
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        template_values = {'username':username, 'email':email}
        error = False
        if(not valid_username(username)):
            template_values['usererror'] = "That's not a valid username"
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
        else: self.redirect("/welcome?username=%(username)s" % {"username": username})

class WelcomeHandler(BaseHandler):
    def get(self):
        username = self.request.get('username')
        self.write("Welcome %(user)s!" % {"user": username})
      