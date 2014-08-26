import webapp2
from dateValidation import valid_month, valid_day, valid_year
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)

birthdayform = """
<!DOCTYPE html>
<html>
	<head>
	    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    	<link type="text/css" rel="stylesheet" href="/stylesheets/udacity.css" />
        <link rel="shortcut icon" type="image/jpeg" href="/static/E.png" />
        <title>Birthday</title> 
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
				<h1>What is your birthday? </h1>
				(Form validation)
				<br>
				<br>
				<form method="post"> 
					<label> Month <input type="text" name="month" value="%(month)s"> </label>
					<label> Day <input type="text" name="day" value="%(day)s"> </label> 
					<label> Year <input type="text" name="year" value="%(year)s"> </label>
					<div style="color: red">%(error)s</div>	
					<br>
					<br>
			        <input type="submit">
				</form>
			</div>
		</div>
	</body>
</html>		
"""    

class BirthdayHandler(webapp2.RequestHandler):
    def write_birthday_form(self, error="", month="", day="", year=""):
        self.response.out.write(birthdayform % {"error": error, "month": escape_html(month), "day": escape_html(day), "year": escape_html(year)})
    def get(self):
        self.write_birthday_form()
    def post(self):
	user_month = self.request.get('month')
	user_day = self.request.get('day')
	user_year = self.request.get('year')
	month = valid_month(user_month)
	day = valid_day(user_day)
        year = valid_year(user_year)
	if not(month and day and year):
            self.write_birthday_form("That doesn't look valid to me, friend.", user_month, user_day, user_year)	
        else: 
            self.redirect("/thanks")       

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

