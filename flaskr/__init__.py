import os
import openai
import json

from flask import Flask, render_template, request

# Configure Flask with URL routes to handle requests.
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        OPENAI_API_KEY='SECRET',
    )
    app.config.from_file('openai-config.json', load=json.load)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Configure OpenAI
    openai.api_key = app.config['OPENAI_API_KEY']
    openai.Model.list()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Show the application's home page, a form to submit to generate a presentation.
    @app.route('/', methods=['GET'])
    def getHome():
        return render_template('index.html')

    # Accept the submitted form and generate a presentation.
    @app.route('/', methods=['POST'])
    def postHome():
        app.logger.debug('Received form: name=' + request.form['name'])
        app.logger.debug('Config DB = ' + app.config['DATABASE'])

        app.logger.debug(openai.Model.list())

        return 'Received form: name=' + request.form['name']

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
