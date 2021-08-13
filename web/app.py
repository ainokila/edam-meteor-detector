#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# export FLASK_APP=web/controller/main
# flask run
# python web/controller/main.py

import os
import json

from flask import Flask
from flask import render_template, request, send_from_directory, url_for


# Import for views
from web.service.views import LastPositiveView, ValidateView, AnalyzerSettingsView
from web.service.views import CCDSettingsView, LoginView, AnalyzeView, LogOutView
from web.service.views import RepositoryTypeView, RepositoryTypeIndividualView, RepositoryView
from source.utils.variables import REPOSITORY_IMG_DATA_PATH, WEB_CONFIG_PATH


template_folder = os.environ['PYTHONPATH'] + '/web/templates'
static_folder = os.environ['PYTHONPATH'] + '/web/static'

app = Flask('meteor_detection_web', 
            template_folder=template_folder,
            static_folder=static_folder)

app.config.from_file(WEB_CONFIG_PATH, load=json.load)

@app.context_processor
def utility_processor():
    def is_active_url(url, selected_class, default=False):
        if url in request.base_url or default:
            return selected_class
    return dict(is_active_url=is_active_url)

@app.route("/views/<img_type>/<img_name>/formats/<extension>")
def get_img(img_type, img_name, extension):

    img_type = os.path.basename(img_type)
    img_name = os.path.basename(img_name)
    extension = os.path.basename(extension)

    path_file = REPOSITORY_IMG_DATA_PATH + '/' + img_type + '/' + img_name + '.' + extension

    if os.path.isfile(path_file):
        return send_from_directory(REPOSITORY_IMG_DATA_PATH + '/' + img_type + '/', img_name + '.' + extension)
    else:
        return send_from_directory(static_folder, 'img/not_found_img.png')



app.add_url_rule('/', view_func=LastPositiveView.as_view('positives_root_view'))
app.add_url_rule('/positives', view_func=LastPositiveView.as_view('positives_view'))
app.add_url_rule('/candidates', view_func=ValidateView.as_view('candidates_view'))

app.add_url_rule('/result_analyze', view_func=AnalyzeView.as_view('analyze_view'))

app.add_url_rule('/repository', view_func=RepositoryView.as_view('repository_view'))
app.add_url_rule('/repository/<img_type>/search', view_func=RepositoryTypeView.as_view('repository_type_view'))
app.add_url_rule('/repository/<img_type>/<img_name>', view_func=RepositoryTypeIndividualView.as_view('repository_type_individual_view'))

app.add_url_rule('/ccd/settings', view_func=CCDSettingsView.as_view('ccd_settings_view'))
app.add_url_rule('/analyzer/settings', view_func=AnalyzerSettingsView.as_view('analyzer_settings_view'))

app.add_url_rule('/login', view_func=LoginView.as_view('login_view'))
app.add_url_rule('/logout', view_func=LogOutView.as_view('logout_view'))


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
    app.run()
