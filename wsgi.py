from flaskr import create_app

# This file exists to create a concrete instance of our app that
# can be used by a WSGI-compatible server like `gunicorn`.
#
# WSGI is a Web Server Gateway Interface, and it is a program that accepts
# web requests and executes Python code in order to serve them. This is needed
# because Python is an interpretted language, not a stand-alone program.

# With this app defined, we can run our program using the command:
# gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
app = create_app()
