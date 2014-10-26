import webapp2
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)


    
rot13 = """<!DOCTYPE html>
<html>
    <head>
        <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
        <link type="text/css" rel="stylesheet" href="/stylesheets/udacity.css" />
        <link rel="shortcut icon" type="image/jpeg" href="/static/E.png" />
        <title>Unit 2 Rot 13</title> 
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="toptoolbar"> 
            <a class = "my_name" href='/'>Evy Kassirer</a> 
            <a class = "section_name" href='/'>About</a>
            <a class = "section_name" href='https://evykassirer.wordpress.com/' target= '_blank'>Blog</a>
            <a class = "section_name" href='/resume' target='_blank'>Resume</a>
            <div class = "dropdown">
                <a class = "section_name" href='/projects'>Projects</a>
                <div class = "dropdownlist">
                    <a href='http://davepagurek.com/yc/' target='_blank'>Code Next</a>
                    <a href='/tictactoe'>Tic Tac Toe</a>
                    <a href='/udacity'>Web Dev</a>
                    <a href='/todo'>Future learning</a>
                </div>
            </div>
            <a class = "section_name" href='https://github.com/evykassirer/', '_blank'>GitHub</a>
            <a class = "section_name" href='http://ca.linkedin.com/in/ekassirer/', '_blank'>LinkedIn</a>
            <a class = "section_name" href='mailto:evy.kassirer@gmail.com' target='_blank'>Email</a>
        </div>
        <div class="toptoolbarsmall"> 
            <div class="my_name">Evy Kassirer</div> 
            <div class = "dropdown">
                <a class = "section_name" href='/projects'>Menu</a>
                <div class = "dropdownlist">
                    <a href='/'>About</a>
                    <a href='https://evykassirer.wordpress.com/' target= '_blank'>Blog</a>
                    <a href='/resume' target='_blank'>Resume</a>
                    <a href='/projects'>Projects</a>
                    <a href='https://github.com/evykassirer/', '_blank'>GitHub</a>
                    <a href='http://ca.linkedin.com/in/ekassirer/', '_blank'>LinkedIn</a>
                    <a href='mailto:evy.kassirer@gmail.com' target='_blank'>Email</a>
                </div>
            </div>
        </div>
        <div class="topplaceholder"></div>
        <div class="pagebody">
            <div class="sidebar">
        		<a href = "/udacity" id="sidebartitle"> Projects: </a>
        		<br>
                <br>
                <a href = "/udacity/rot13">Rot13</a>
                <br>
                <a href = "/udacity/birthday">Do you know your birthday?</a>
                <br>
        		<a href = "/udacity/asciichan">ASCIICHAN!</a>
        		<br>
        		<a href = "/udacity/blog">The blog (main course project)</a>
        		<br>
        		<a href = "/udacity/wiki">Wiki (course exam)</a>
            </div>
            <div class="content">
                Enter some text to ROT13:

                (Try pressing submit again after you encode your text)
                <br>
                <br>
                <form method="post">    
                    <textarea name="text" style="height: 100px; width: 400px;">%(input)s</textarea> 
                    <br>
                    <input type="submit">
                </form>
            </div> 
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

