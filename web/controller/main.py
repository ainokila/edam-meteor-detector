#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# export FLASK_APP=web/controller/main
# flask run
# python web/controller/main.py

import os
from flask import jsonify

from flask import Flask, url_for, request, redirect, session, abort

#TODO: Move to service model
from flask import render_template

from source.db.userdb import UserDB
from web.service.forms import ConfigCCDForm, LoginForm


template_folder = os.environ['PYTHONPATH'] + '/web/templates'
static_folder = os.environ['PYTHONPATH'] + '/web/static'

app = Flask(__name__, 
            template_folder=template_folder,
            static_folder=static_folder)

#TODO: Move to secret env value
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4b'


def get_user(username):
    user = None
    try:
        userdb = UserDB()
        user = userdb.get_user(username)
    finally:
        userdb._close_db()
    return user

def is_auth():
    username = session.get('username', None)
    password = session.get('password', None)

    if not username or not password:
        return False

    user = get_user(username)

    return user and user.password == password

def session_user():
    return get_user(session['username'])

@app.route('/')
def index():
    return explore()


@app.route('/explore')
def explore():
    user = None
    if is_auth():
        user = session_user()
    return render_template('show_photo.html', user=user)

@app.route('/validate')
def validate_photos():
    if is_auth():
        user = session_user()
        return render_template('analyze_photos.html', user=user)
    else:
        abort(403, description="Login required")

@app.route('/result_analyze', methods=['GET', 'POST'])
def result_analyze():
    if is_auth():
        result = {
            'new_photo': 'https://s3-us-west-2.amazonaws.com/melingoimages/Images/87718.jpg',
            'id_photo': '12345' 
        }
        return jsonify(result)
    else:
        abort(403, description="Login required")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if is_auth():
        user = session_user()
        form = ConfigCCDForm()
        if form.validate_on_submit():
            print("Bieeen")
            return render_template('settings.html', user=user, form=form)
        else:
            return render_template('settings.html', user=user, form=form)
        
    else:
        abort(403, description="Login required")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_user(username)

        if user and user.password == password:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('explore'))
        else:
            return render_template('login.html', form=form, incorrect_login=True)

        return redirect('/success')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('show_photo.html', name='A')


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def forbidden(e):
    return render_template('403.html'), 403

app.register_error_handler(404, page_not_found)
app.register_error_handler(403, forbidden)

if __name__ == "__main__":
    app.run(debug=True)
