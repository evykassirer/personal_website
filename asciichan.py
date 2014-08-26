import os
import webapp2
import jinja2
import urllib2
import logging
import time
from xml.dom import minidom
from google.appengine.api import memcache
from google.appengine.ext import db
    
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

IP_URL = "http://api.hostip.info/?ip="                               
def get_coords(ip):
    ip = "4.2.2.2"
    ip = "23.24.209.141"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    
    if content:
        x = minidom.parseString(content)
        coords = x.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            c = str(coords[0].childNodes[0].nodeValue).split(",", 1)
            return db.GeoPt(c[1], c[0]) 

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"

def gmaps_img(points):
    url = GMAPS_URL
    for p in points:
        url += "&markers=%s,%s" %(p.lat, p.lon)
    return url
    
class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

def top_arts(update=False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")
        arts = list(arts) 
        #this makes it a list so we're not doing the query every time we iterate
        memcache.set(key, arts)
    return arts
    
class AsciichanHandler(BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()         
        #find which arts have coords
        points = []
        for a in arts:
            if a.coords:
                points.append(a.coords)
                
        #if we have any arts coords, make an image url
        img_url = None
        if points:
            img_url = gmaps_img(points)               
        self.render("/udacity/frontascii.html", title=title, art=art, error=error, arts=arts, img_url=img_url)
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            a = Art(title=title, art=art)
            #lookup the user's coordinates by IP
            coords = (get_coords(self.request.remote_addr))
            if coords:
                a.coords = coords
            a.put() #puts in database
            top_arts(True)
            time.sleep(0.1)
            self.redirect("/asciichan")
        else:
            error = "we need both a title annd some artwork!"
            self.render_front(title, art, error)
        #if title and art:
        #    self.redirect("/asciichan")