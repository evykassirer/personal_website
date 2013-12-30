import os
import webapp2
import cgi
import jinja2
from rot13 import Rot13Handler
from birthday import BirthdayHandler, ThanksHandler
from signup import SignUpHandler, WelcomeHandler
from asciichan import AsciichanHandler
from blog import BlogFront, NewPost, PostPage, error404handler

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


app = webapp2.WSGIApplication([(r'/', MainPage),
                                (r'/birthday', BirthdayHandler),
                                (r'/thanks', ThanksHandler), 
                                (r'/rot13', Rot13Handler),
                                (r'/signup', SignUpHandler), 
                                (r'/welcome', WelcomeHandler),
                                (r'/asciichan', AsciichanHandler),
                                (r'/blog', BlogFront),
                                (r'/blog/newpost', NewPost),
                                (r'/blog/404error', error404handler),
                                (r'/blog/post/(\d+)', PostPage)], debug=True)
