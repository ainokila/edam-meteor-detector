#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# export FLASK_APP=web/controller/main
# flask run 
# python web/controller/main.py

import os

from flask import Flask, url_for
from markupsafe import escape

#TODO: Move to service model
from flask import render_template

template_folder = os.environ['PYTHONPATH'] + '/web/templates'
static_folder = os.environ['PYTHONPATH'] + '/web/static'

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

@app.route('/')
def index():
    return render_template('dashboard.html', name='A')

@app.route('/explore')
def explore():
    return render_template('dashboard.html', name='A')

@app.route('/validate')
def validate_photos():
    return render_template('dashboard.html', name='A')

@app.route('/settings')
def settings():
    return render_template('dashboard.html', name='A')

@app.route('/login')
def login():
    return 'login'


if __name__ == "__main__":
    app.run(debug=True)