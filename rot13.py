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
    </head>
    
    <body>
        <div class="toptoolbar"> 
            <div id="my_name">Evy Kassirer</div> 
            <div class = "section_name" onclick="window.location = '/';">About</div>
            <div class = "section_name" onclick="window.open('https://evykassirer.wordpress.com/', '_blank');">Blog</div>
            <div class = "section_name" onclick="window.open('/resume', '_blank');">Resume</div>
            <div class = "dropdown">
                <div class = "section_name" onclick="window.location = '/';">Projects</div>
                <ul>
                    <li onclick="window.location = '/tictactoe';">Tic Tac Toe</li>
                    <li onclick="window.location = '/udacity';">Web Dev</li> 
                    <!-- Web Development - Udacity Course Projects ~~ need to fix line wrapping issue  --> 
                    <li onclick="window.open('http://davepagurek.com/yc/', '_blank');">Code Next</li>
                    <li onclick="window.location = '/todo';">Future learning</li> <!-- Programming To Do List <br> && Coding Resources -->
                    <!-- put what languages are on the projects ~~ maybe make a projects page-->
                </ul>
            </div>
            <div class = "section_name" onclick="window.open('https://github.com/evykassirer/', '_blank');">GitHub</div>
            <div class = "section_name" onclick="window.open('http://ca.linkedin.com/in/ekassirer/', '_blank');">LinkedIn</div>
            <div class = "section_name" onclick="window.open('mailto:evy.kassirer@gmail.com', '_blank');">Email</div>
        </div>
        <div class="topplaceholder"></div>
        <div class="pagebody">
            <div class="sidebar">
        		<a href = "/udacity" id="sidebartitle"> Projects: </a>
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

