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
from wiki import WikiFront, WikiPostPage, WikiEditPost
from wikisignup import WikiSignUpHandler
from wikilogin import WikiLogInHandler, WikiLogOutHandler

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
        self.render("frontpage.html")
        
class MainUdacityPage(BaseHandler):
    def get(self):
        self.render("udacity/welcome.html")       

class Resume(BaseHandler):
    def get(self):
      self.render("resume.html") 
      
class ToDo(BaseHandler):
    def get(self):
      self.render("todo.html") 

class Projects(BaseHandler):
    def get(self):
      self.render("projects.html") 

class TicTacToe(BaseHandler):
    def get(self):
      self.render("tick-tack-toe.html")         
      
class XTicTacToe(BaseHandler):
    def get(self):
      self.render("super-ttt.html") 
      
PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'
        
app = webapp2.WSGIApplication([(r'/', MainPage),
                                (r'/todo/?', ToDo),
                                (r'/projects/?', Projects),
                                (r'/resume/?', Resume),
                                (r'/tictactoe/?', TicTacToe),
                                (r'/extreme_tictactoe/?', XTicTacToe),
                                (r'/404error/?', error404handler),
                                #udacity course stuff
                                (r'/udacity/?', MainUdacityPage),
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
                                (r'/wiki/?', WikiFront),
                                (r'/wiki/signup/?', WikiSignUpHandler),
                                (r'/wiki/logout/?', WikiLogOutHandler),
                                (r'/wiki/login/?', WikiLogInHandler),
                                (r'/wiki/_edit/' + PAGE_RE, WikiEditPost),
                                (r'/wiki/' + PAGE_RE, WikiPostPage),
                                ], debug=True)
