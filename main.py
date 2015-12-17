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
      
class Resources(BaseHandler):
    def get(self):
      self.render("resources.html") 

class Projects(BaseHandler):
    def get(self):
      self.render("projects.html") 

class TicTacToe(BaseHandler):
    def get(self):
      self.render("tick-tack-toe.html")         
      
class XTicTacToe(BaseHandler):
    def get(self):
      self.render("super-ttt.html") 

class blogMain(BaseHandler):
    def get(self):
      self.render("blog.html") 

class blogPost(BaseHandler):
    def get(self, post_id):
        if (os.path.isfile("templates/blog-post-"+post_id+".html")) :
            self.render("blog-post-"+post_id+".html")
        else:
            self.redirect("/blog")

class contactPage(BaseHandler):
    def get(self):
        self.render("contact.html")

class musicPage(BaseHandler):
    def get(self):
        self.render("music.html")
      
PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'
        
app = webapp2.WSGIApplication([(r'/', MainPage),
                                #udacity course stuff
                                (r'/udacity/?', MainUdacityPage),
                                (r'/udacity/birthday/?', BirthdayHandler),
                                (r'/udacity/thanks/?', ThanksHandler), 
                                (r'/udacity/rot13/?', Rot13Handler),
                                (r'/udacity/asciichan/?', AsciichanHandler),
                                (r'/udacity/blog?(?:/\.json)?', BlogFront),
                                (r'/udacity/blog/newpost/?', NewPost),
                                (r'/udacity/blog/post/(\d+)(?:\.json)?', PostPage),
                                (r'/udacity/blog/signup/?', SignUpHandler), 
                                (r'/udacity/blog/welcome/?', WelcomeHandler),
                                (r'/udacity/blog/login/?', LogInHandler),
                                (r'/udacity/blog/logout/?', LogOutHandler),
                                (r'/udacity/blog/flush/?', flushHandler),
                                (r'/udacity/wiki/?', WikiFront),
                                (r'/udacity/wiki/signup/?', WikiSignUpHandler),
                                (r'/udacity/wiki/logout/?', WikiLogOutHandler),
                                (r'/udacity/wiki/login/?', WikiLogInHandler),
                                (r'/udacity/wiki/_edit/' + PAGE_RE, WikiEditPost),
                                (r'/udacity/wiki/' + PAGE_RE, WikiPostPage),
                                #my stuff
                                (r'/resources/?', Resources),
                                (r'/blog/?', blogMain),
                                (r'/blog/(.*)/?', blogPost),
                                (r'/projects/?', Projects),
                                (r'/tictactoe/?', TicTacToe),
                                (r'/extreme_tictactoe/?', XTicTacToe),
                                (r'/contact/?', contactPage),
                                (r'/music/?', musicPage),
                                (r'/404error/?', error404handler),
                                (r'/.*', error404handler),
                                ], debug=True)
