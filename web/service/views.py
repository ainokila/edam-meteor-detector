#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

from flask.views import View, MethodView
from flask import render_template, session, redirect, url_for, redirect, jsonify, abort, request


from source.db.userdb import UserDB
from web.service.forms import ConfigCCDForm, LoginForm

# TODO: Move to a config file or something similar
STATIC_PATH = os.environ['PYTHONPATH'] + '/web/static'
RAW_PATH = STATIC_PATH + '/data/raw/'
CANDIDATES_PATH = STATIC_PATH + '/data/candidates/'
POSITIVES_PATH = STATIC_PATH + '/data/positives/'


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


def _get_image_name(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                return file
    return None

def _move_image(src_path_name, dst_path_name):
    os.rename(src_path_name, dst_path_name)

def _delete_image(src_path_name):
    os.remove(src_path_name)

class ExploreView(View):

    methods = ['GET']

    def get_template_name(self):
        return 'show_photo.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        user = None
        if is_auth():
            user = session_user()
        context = { "user": user }
        return self.render_template(context)
    

class ValidateView(View):

    methods = ['GET']

    def get_template_name(self):
        return 'analyze_photos.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if is_auth():
            img = _get_image_name(CANDIDATES_PATH)
            if img:
                img = url_for("static", filename='data/candidates/' + img)
            context = { "user": session_user(), "img": img}
            return self.render_template(context)
        else:
            abort(403, description="Login required")


class SettingsView(View):

    methods = ['GET', 'POST']

    def get_template_name(self):
        return 'settings.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if is_auth():
            user = session_user()
            form = ConfigCCDForm()
            context = { 'user': user, 'form': form}
            if form.validate_on_submit():
                print("Bieeen")
                return self.render_template(context)
            else:
                print("mal")
                return self.render_template(context)
            
        else:
            abort(403, description="Login required")


class LoginView(View):

    methods = ['GET', 'POST']

    def get_template_name(self):
        return 'login.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = get_user(username)

            if user and user.password == password:
                session['username'] = username
                session['password'] = password
                return redirect(url_for('explore_view'))
            else:
                context = {'form': form, 'incorrect_login': True}
                return self.render_template(context)

        return render_template('login.html', form=form)


class LogOutView(MethodView):

    def get(self):
        session.clear()
        return redirect(url_for('explore_root_view'))


class AnalyzeView(MethodView):

    def post(self):
        if is_auth():
            # Check if it is positive or negative
            data = json.loads(request.get_data())

            filename = data['photo'].split('/')[-1]
            path_name = CANDIDATES_PATH + filename

            if data['positive']:
                _move_image(path_name, POSITIVES_PATH + filename)
                print("Moving photo")
            else:
                print("Removing photo")
                _delete_image(path_name)

            img = _get_image_name(CANDIDATES_PATH)
            result = {
                'new_photo': url_for("static", filename='data/candidates/' + img),
                'id_photo': '12345' 
            }
            return jsonify(result)
        else:
            abort(403, description="Login required")