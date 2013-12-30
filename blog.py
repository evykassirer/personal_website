import os
import webapp2
import jinja2

from google.appengine.ext import db
    
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
      
class Post(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
               
class BlogFront(BaseHandler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC limit 10")
        self.render("front.html", posts=posts)
    def get(self):
        self.render_front()        

class PostPage(BaseHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id)) 
        if not post:
            self.redirect("blog/404error")
            return
        self.render("singlepost.html", post=post)
        
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
            self.redirect("/blog/post/" + str(id))
        else:
            error = "Please enter both a title and a body for your blog post!"
            self.render_newpost(title, body, error)

class error404handler(BaseHandler):
    def get(self):
        self.render("404Error.html")