import webapp2
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)
    
rot13 = """<!DOCTYPE html>
<html>
    <head>
        <title>Unit 2 Rot 13</title> 
    </head>
    <body>
        <h2>Enter some text to ROT13:</h1>
        <form method="post">    
            <textarea name="text" style="height: 100px; width: 400px;">%(input)s</textarea> 
            <br>
            <input type="submit">
        </form>
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

