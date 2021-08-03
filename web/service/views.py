#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

from werkzeug.datastructures import MultiDict
from flask.views import View, MethodView
from flask import render_template, session, redirect, url_for, redirect, jsonify, abort, request


from source.db.userdb import UserDB
from source.model.repository import ImageRepository
from source.model.image.fits import ImageFits
from source.utils.variables import CLIENT_CONFIG_PATH, ANALYZER_CONFIG_PATH
from source.model.ccdconfig import CCDConfig


from web.service.forms import ConfigCCDForm, LoginForm


image_repository = ImageRepository()


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


def get_images(img_type, offset, size):

    if img_type == ImageRepository.POSITIVES:
        img_path = 'data/positives/'
    elif img_type == ImageRepository.CANDIDATES:
        img_path = 'data/candidates/'
    else:
        raise Exception('Incorrect img_type')

    images = image_repository.list_files(img_type, extension='jpg')
    images_with_header = []
    if images:
        for image in images:
            filename = img_path + image
            img = url_for("static", filename=filename)
            header = get_header(path_file=img_type + image.split('.')[-2] + '.fit')
            images_with_header.append({'img': img, 'header': header})

    return images_with_header[offset:offset+size]


def get_image(img_type, img_name):
    if img_type == ImageRepository.POSITIVES:
        img_path = 'data/positives/'
    elif img_type == ImageRepository.CANDIDATES:
        img_path = 'data/candidates/'
    else:
        raise Exception('Incorrect img_type')

    image = image_repository.find_file(img_type, img_name, extension='jpg')
    filename = img_path + image
    img = url_for("static", filename=filename)
    header = get_header(path_file=img_type + image.split('.')[-2] + '.fit')
    return {'img': img, 'header': header}

def last_positive():
    images = image_repository.list_files(ImageRepository.POSITIVES, extension='jpg')
    img = None
    header = None
    if images:
        filename = 'data/positives/' + images[0]
        img = url_for("static", filename=filename)
        header = get_header(path_file=ImageRepository.POSITIVES + images[0].split('.')[-2] + '.fit')
    return img, header

def next_candidate_image():
    images = image_repository.list_files(ImageRepository.CANDIDATES, extension='jpg')
    img = None
    header = None
    if images:
        filename = 'data/candidates/' + images[0]
        img = url_for("static", filename=filename)
        header = get_header(path_file=ImageRepository.CANDIDATES + images[0].split('.')[-2] + '.fit')
    return img, header

def get_header(path_file):
    fits = ImageFits()
    fits.load_data_from_file(path_file)
    return fits.header

class LastPositiveView(View):

    methods = ['GET']

    def get_template_name(self):
        return 'show_photo.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        user = None
        img, header = last_positive()
        name = img.split('.')[-2].split('/')[-1]
        context = { "img": img, "name":name, "header":header}
        if is_auth():
            user = session_user()
        context.update({ "user": user })
        return self.render_template(context)
    

class ValidateView(View):

    methods = ['GET']

    def get_template_name(self):
        return 'validate_photos.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if is_auth():
            img, header = next_candidate_image()
            name = img.split('.')[-2].split('/')[-1]
            context = { "user": session_user(), "img": img, "name":name, "header":header}
            return self.render_template(context)
        else:
            abort(403, description="Login required")


class CCDSettingsView(View):

    methods = ['GET', 'POST']

    def get_template_name(self):
        return 'settings_ccd.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if is_auth():

            user = session_user()
            form = ConfigCCDForm()

            if request.method == 'POST':
                context = { 'user': user, 'form': form}

                if form.validate_on_submit():
                    CCDConfig(form._to_dict()).export_to_file(CLIENT_CONFIG_PATH)
                
                return self.render_template(context)

            else:
                ccd_conf = CCDConfig.create_from_file(CLIENT_CONFIG_PATH)
                form = ConfigCCDForm(formdata=MultiDict(ccd_conf.to_dict()))
                context = { 'user': user, 'form': form}
                return self.render_template(context)

        else:
            abort(403, description="Login required")

class AnalyzerSettingsView(View):

    methods = ['GET', 'POST']

    def get_template_name(self):
        return 'settings_analyzer.html'

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if is_auth():

            user = session_user()
            form = ConfigCCDForm()

            if form.validate_on_submit():
                context = { 'user': user, 'form': form}
                CCDConfig(form._to_dict()).export_to_file(CLIENT_CONFIG_PATH)
                return self.render_template(context)

            else:
                ccd_conf = CCDConfig.create_from_file(CLIENT_CONFIG_PATH)
                form = ConfigCCDForm(formdata=MultiDict(ccd_conf.to_dict()))
                context = { 'user': user, 'form': form}
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
                return redirect(url_for('positives_view'))
            else:
                context = {'form': form, 'incorrect_login': True}
                return self.render_template(context)

        return render_template('login.html', form=form)


class LogOutView(MethodView):

    def get(self):
        session.clear()
        return redirect(url_for('positives_root_view'))


class AnalyzeView(MethodView):

    def post(self):
        if is_auth():
            # Check if it is positive or negative
            data = json.loads(request.get_data())

            filename = data['photo'].split('.')[-2].split('/')[-1]

            if data['positive']:
                img_destination = ImageRepository.POSITIVES
            else:
                img_destination = ImageRepository.DISCARDED

            image_repository.move_files(filename, ImageRepository.CANDIDATES, img_destination)

            img, header = next_candidate_image()
            result = {
                'photo': img,
                'name': filename,
                'header': header.to_dict() if header else {}
            }
            return jsonify(result)
        else:
            abort(403, description="Login required")


#TODO: Improve this
type_mapping = {
    'candidates': ImageRepository.CANDIDATES,
    'positives': ImageRepository.POSITIVES,
}

type_auth = {
    'candidates': False,
    'positives': True,
}


class RepositoryView(MethodView):

    def post(self, img_type):
        if img_type in type_mapping:
            if not type_auth[img_type] or is_auth():

                data = json.loads(request.get_data())
                offset = data.get('offset', 0)
                size = data.get('size', 0)

                result = {'data': [] }
                for img_result in get_images(type_mapping[img_type], offset, size):
                    result['data'].append(
                        {
                            'photo': img_result['img'],
                            'header': img_result['header'].to_dict() if img_result['header'] else {}
                        }
                    )

                return jsonify(result)
            else:
                abort(403, description="Login required")
        else:
            abort(404, description="Path not found")

class RepositoryIndividualView(MethodView):

    def get(self, img_type, img_name):
        if img_type in type_mapping:
            if not type_auth[img_type] or is_auth():
                image = get_image(type_mapping[img_type], img_name)                
                result = {
                    'photo': image['img'],
                    'name': img_name,
                    'header': image['header'].to_dict() if image['header'] else {}
                }
                return jsonify(result)
            else:
                abort(403, description="Login required")
        else:
            abort(404, description="Path not found")