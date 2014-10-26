import webapp2
from dateValidation import valid_month, valid_day, valid_year
import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)

birthdayform = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
        <link rel="stylesheet" type="text/css" href="/stylesheets/main.css" />
        <link rel="shortcut icon" type="image/jpeg" href="/static/E.png" />
        <link type="text/css" rel="stylesheet" href="/stylesheets/udacity.css" />
        <title>Birthday</title> 
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

