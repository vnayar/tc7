import os
import openai
import json

# The @dataclass annotiation defines __init__ for simple classes.
from dataclasses import dataclass, field
from datetime import date
from flask import Flask, render_template, request

from flaskr.latex_beamer import LatexBeamer;

# Configure Flask with URL routes to handle requests.
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        OPENAI_TEST_DATA=False,
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
        app.logger.debug("Received request: ", request.form.to_dict)
        
        myPrompt = """
        My business, "{}", has the following vision: <| {} |>

        Customers have a problem: <| {} |>

        My business solves this problem by: <| {} |>

        """.format(
            request.form['name'],
            request.form['vision'],
            request.form['problem'],
            request.form['solution'])

        if request.form['advantage']:
            myPrompt += """
            Our business has the following competitive advantages: <| {} |>
            """.format(request.form['advantage'])

        if request.form['market']:
            myPrompt += """
            The following is known about the business market: <| {} |>

            """.format(request.form['market'])

        if request.form['team']:
            myPrompt += """
            The team behind the business is: <| {} |>

            """.format(request.form['team'])

        myPrompt += """
        Create a pitch deck for my business to be presented to investors.

        The pitch deck should have slides for the: problem, solution, market, product, business
        model, competitive advantages, team, and business model.

        Each slide should be in the following format:
        
        Slide 1: Slide Title
        - A relevant point.
        - Additional points...

        """

        # Use a fake OpenAPI response to save credits during development.
        if app.config['OPENAI_TEST_DATA']:
            completion = type('Completion', (object,), {
	        "choices": [
	            type('Choice', (object,), {
	                "text": """
	                    Slide 1: Ham on Rye
	                    - I Like Ham.
	                    - Ham is good.
	                    Slide 2: Ham on Ham
	                    - Bacon is also good.
	                    - Are fish bacon?
	                    Slide 3: Rye on Ham
	                    - Are you a fish?
	                    - Can fish eat bread?
	                    """
	            })
	        ]
	    })
        else:
            # Using our prompt, call OpenAI to get a probable word completion (an answer).
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=myPrompt,
                max_tokens=2048,
                temperature=0
            )

        @dataclass
        class Slide:
            title: str
            items: list[str] = field(default_factory=list)

        slides: list[Slide] = []
        for line in completion.choices[0].text.split("\n"):
            line = line.strip()
            if line.startswith("Slide "):
                slides.append(Slide(line.split(":", 1)[1].strip()))
            elif line.startswith("- "):
                slide = slides[-1]
                slide.items.append(line.split("- ", 1)[1])

        app.logger.debug("Extracted Slide Data:")
        app.logger.debug(slides)

        # Write the slide data into a new LaTeX document in beamer syntax.
        latex = LatexBeamer()
        latex.startDoc()
        latex.writePreamble(
            title=request.form['name'],
            subtitle=request.form['vision'],
            date=date.today())
        latex.startBody()
        for slide in slides:
            latex.addSlide(slide.title, slide.items)
        latex.endBody()
        file = latex.endDoc()
        app.logger.debug("Temporary file: ")
        app.logger.debug(file)
        return slides

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
