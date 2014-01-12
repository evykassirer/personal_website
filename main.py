#to do
#link back to main on each page

import os
import webapp2
import cgi
import jinja2
from rot13 import Rot13Handler
from birthday import BirthdayHandler, ThanksHandler
from signup import SignUpHandler, WelcomeHandler
from asciichan import AsciichanHandler
from blog import BlogFront, NewPost, PostPage, error404handler, flushHandler
from login import LogInHandler, LogOutHandler

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
        
class MainPage(BaseHandler):
    def get(self):
        self.render("welcome.html")

class RedirectHandler(BaseHandler):
    def get(self):
        url = self.request.get("url")
        self.redirect(str(url))        

app = webapp2.WSGIApplication([(r'/', MainPage),
                                (r'/birthday/?', BirthdayHandler),
                                (r'/thanks/?', ThanksHandler), 
                                (r'/rot13/?', Rot13Handler),
                                (r'/asciichan/?', AsciichanHandler),
                                (r'/blog?(?:/\.json)?', BlogFront),
                                (r'/blog/newpost/?', NewPost),
                                (r'/blog/post/(\d+)(?:\.json)?', PostPage),
                                (r'/blog/signup/?', SignUpHandler), 
                                (r'/blog/welcome/?', WelcomeHandler),
                                (r'/blog/login/?', LogInHandler),
                                (r'/blog/logout/?', LogOutHandler),
                                (r'/blog/flush/?', flushHandler),
                                (r'/redirect/?', RedirectHandler),
                                (r'/blog/404error/?', error404handler)
                                ], debug=True)
