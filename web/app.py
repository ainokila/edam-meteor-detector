#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# export FLASK_APP=web/controller/main
# flask run
# python web/controller/main.py

import os
from flask import Flask

from flask import render_template

# Import for views
from web.service.views import ExploreView, ValidateView, SettingsView, LoginView, AnalyzeView, LogOutView


template_folder = os.environ['PYTHONPATH'] + '/web/templates'
static_folder = os.environ['PYTHONPATH'] + '/web/static'

app = Flask(__name__, 
            template_folder=template_folder,
            static_folder=static_folder)

#TODO: Move to secret env value
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4b'


app.add_url_rule('/', view_func=ExploreView.as_view('explore_root_view'))
app.add_url_rule('/explore', view_func=ExploreView.as_view('explore_view'))
app.add_url_rule('/validate', view_func=ValidateView.as_view('validate_view'))
app.add_url_rule('/settings', view_func=SettingsView.as_view('settings_view'))
app.add_url_rule('/result_analyze', view_func=AnalyzeView.as_view('analyze_view'))

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
    app.run(debug=True)
