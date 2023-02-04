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

6. Put your API key into the file `instance/openai-config.json` like so:
```
 {
  "OPENAI_API_KEY": "MY_API_KEY"
 }
```

## Local Setup

1. Load the python virtual environment.
`source bin/activate`

2. Run the server locally.
`flask --app flaskr --debug run`

3. Visit the server at http://127.0.0.1:5000/

## Deployment on AWS

The deployment of this app is based on
[AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) and follows the
method outlined in the
[online tutorial](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html).

1. Install the AWS Elastic Beanstalk command-line tool following these instructions:
   https://github.com/aws/aws-elastic-beanstalk-cli-setup
2. Configure the `eb` tool for your AWS account.
