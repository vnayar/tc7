#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app
