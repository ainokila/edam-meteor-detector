#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# export FLASK_APP=web/controller/main
# flask run
# python web/controller/main.py

import os

from flask import Flask, url_for, request, redirect

#TODO: Move to service model
from flask import render_template

template_folder = os.environ['PYTHONPATH'] + '/web/templates'
static_folder = os.environ['PYTHONPATH'] + '/web/static'

app = Flask(__name__, template_folder=template_folder,
            static_folder=static_folder)


@app.route('/')
def index():
    return explore()


@app.route('/explore')
def explore():
    return render_template('latest_photo.html', name='A')


@app.route('/validate')
def validate_photos():
    return render_template('explore_photos.html', name='A')


@app.route('/settings')
def settings():
    return render_template('settings.html', name='A')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate the user and redirect
        return redirect(url_for('explore'))
    else:
        return render_template('login.html', name='A')


if __name__ == "__main__":
    app.run(debug=True)
