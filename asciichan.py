import os
import webapp2
import jinja2

from google.appengine.ext import db
    
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

class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
               
class AsciichanHandler(BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("frontascii.html", title=title, art=art, error=error, arts=arts)
    def get(self):
        self.render_front()
        #self.response.out.write("hi")        
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            a = Art(title=title, art=art)
            a.put() #puts in database
            self.redirect("/asciichan")
            #self.write("thanks!")
        else:
            error = "we need both a title annd some artwork!"
            self.render_front(title, art, error)