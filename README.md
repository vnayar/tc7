## Project Setup

1. Create a virtual environment.
`python3 -m venv venv`

2. Activate the environment.
`source venv/bin/activate`

3. Install flask
`pip install flask`

4. Install openai.
`pip install openai`

5. Obtain an API Key from OpenAI: https://platform.openai.com/account/api-keys

6. Put your API key into the file `instance/openai-config.json`.

## Local Setup

1. Load the python virtual environment.
`source bin/activate`

2. Run the server locally.
`flask --app flaskr --debug run`

3. Visit the server at http://127.0.0.1:5000/
