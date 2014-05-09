import webapp2
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)


    
rot13 = """<!DOCTYPE html>
<html>
    <head>
        <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
        <title>Unit 2 Rot 13</title> 
    </head>
    
    <body>
        <div class="header">Enter some text to ROT13:</div>
        <div class="pagebody">
		(Try pressing submit again after you encode your text)
        <br>
        <br>
        <form method="post">    
            <textarea name="text" style="height: 100px; width: 400px;">%(input)s</textarea> 
            <br>
            <input type="submit">
        </form>
        </div>
        
        <div class="sidebar">
		Projects:
		<br>
        <br>
        <a href = "/rot13">Rot13</a>
        <br>
        <a href = "/birthday">Do you know your birthday?</a>
        <br>
		<a href = "/asciichan">ASCIICHAN!</a>
		<br>
		<a href = "/blog">The blog (main course project)</a>
		<br>
		<a href = "/wiki">Wiki (course exam)</a>
        <br>
		<a href = "/udacity">Go back </a>
        </div> 
    </body>
</html>
"""  

def convert_lower_char(c):
    return chr(ord('a') + (((ord(c) - ord('a')) + 13) % 26))

def convert_upper_char(c):
    return chr(ord('A') + (((ord(c) - ord('A')) + 13) % 26))
    
alpha = "abcdefghijklmnopqrstuvwxyz"    
    
def convert_text(s):
    i = 0
    while i < len(s):
        if s[i] in alpha:
            s = s[:i] + convert_lower_char(s[i]) + s[(i+1):]
        if s[i] in alpha.upper():
            s = s[:i] + convert_upper_char(s[i]) + s[(i+1):]
        i = i + 1
    return s
        
class Rot13Handler(webapp2.RequestHandler):
    def write_rot13_form(self, input=""):
        self.response.out.write(rot13 % {"input": escape_html(input)})
    def get(self):
		self.write_rot13_form()
    def post(self):
	    input = self.request.get('text')
	    self.write_rot13_form(convert_text(input))

