#!/bin/sh

python3 manage.py migrate
python3 manage.py makesuper
gunicorn newsscraper.wsgi --bing=0.0.0.0:80