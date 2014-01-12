udacitycs253
============
Web Development Course Files


This is a series of small projects plus a blog application 
that were created as part of a udacity.com course (CS253 Web Development).

Old Stuff: a few files I was using during lessons, but weren't worth 
putting on the website. 

Stylesheets: these were created by the instructor of the course, although 
I mostly understnad them, I didn't write them. Currently there is only a 
main stylesheet which is included on the pages of the blog.

Templates: This is the html for most (if not all) of the pages, 
inserted into the main code as needed.

app.yaml is the code that pretty much is the base information for the app. 
Here I state the name of the application, include jinja (which lets me use templates), 
and refer to the path of the stylesheets folder.

birthday (incl. date validation) and rot13 were assignments that were not part of the blog applicaton.
asciichan was an introduction to creating the blog structure, and I kept it because it's cool. 
It's supposedly a place where people post ascii art.

The blog is the main project, with 
login (which enables cookies)
signup (which creates an entry in the user database),
and the ability to create posts.
(However, the fact that you are logged in currently does nothing but redirect to a welcome page, 
soon this should give you permission to create posts and put the users name with the post.)

There is still lots to come, hopefully :)