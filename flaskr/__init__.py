import os
import io
import openai
import json
import requests

import pandoc
from pdflatex import PDFLaTeX

from tempfile import NamedTemporaryFile, gettempdir
from werkzeug.utils import secure_filename

# The @dataclass annotiation defines __init__ for simple classes.
from dataclasses import dataclass, field
from datetime import date
from flask import Flask, render_template, request, send_file

from flaskr.latex_beamer import createPitchDeckLatexFile;
from flaskr.gpt import GptService
from flaskr.pitchdeck import Slide, PitchDeck, parseSlides

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

    ## Configure OpenAI
    #openai.api_key = app.config['OPENAI_API_KEY']

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
        app.logger.debug("Received request.form: ", request.form.to_dict)
        gptService = GptService(app.config)

        myPrompt = gptService.buildPitchDeckPrompt(
            name=request.form['name'],         # required
            vision=request.form['vision'],     # required
            problem=request.form['problem'],   # required
            solution=request.form['solution'], # required
            advantage=request.form.get('advantage', ''),
            market=request.form.get('market', ''),
            team=request.form.get('team', ''),
        )

        completion = gptService.createCompletion(myPrompt)

        # Extract the logo from the form and make it available.
        # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
        logoFileName = ''
        print('LogoCheck 1:')
        if 'logo' in request.files:
            print('LogoCheck 2:')
            logoFile = request.files['logo']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if logoFile.filename != '':
                print('LogoCheck 3:')
                filename = secure_filename(logoFile.filename)
                logoFileName = os.path.join(gettempdir(), filename)
                logoFile.save(logoFileName)
        print('LogoCheck 4:')

        # Use GPT's output to create our slides.
        slides = parseSlides(completion.choices[0].text)

        # Supplement a few slides with images.
        i = 0
        for slide in slides:
            i = i + 1
            if i % 2 == 0:
                continue
            imagePrompt = ' '.join(slide.items)
            image = gptService.createImage(imagePrompt)
            req = requests.get(image.data[0].url, allow_redirects=True)
            imageFile = NamedTemporaryFile(suffix=".png", mode="wb", delete=False)
            imageFile.write(req.content)
            imageFile.close()
            slide.imageFileName = imageFile.name

        pitchDeck = PitchDeck(
            title = request.form['name'],
            subtitle = request.form['vision'],
            date = date.today(),
            logoFileName = logoFileName,
            slides = slides)

        # Write the slide data into a new LaTeX document in beamer syntax.
        latexFile = createPitchDeckLatexFile(pitchDeck)

        if request.form['format'] == 'pptx':
            # TODO: Pandoc currently does NOT preserve icons, pictures, or other graphics.
            #       Find a replacement or some other mechanism to convert from LaTeX to PPTX.
            # Convert the temporary file into powerpoint.
            # TODO: Use the existing file rather than re-opening it to read it.
            doc = pandoc.read(file=latexFile.name, format="latex")
            tempFile = NamedTemporaryFile(suffix=".pptx", mode="wt", encoding="utf-8", delete=False)
            tempFile.close()
            pandoc.write(doc, file=tempFile.name, format="pptx")
            return send_file(tempFile.name, mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        elif request.form['format'] == 'pdf':
            # Convert the temporary file into a PDF.
            # See: https://pypi.org/project/pdflatex/
            pdfl = PDFLaTeX.from_texfile(latexFile.name)
            pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
            return send_file(io.BytesIO(pdf), download_name=pitchDeck.title + '.pdf', mimetype='application/pdf')
        else:
            return 'oops'

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
