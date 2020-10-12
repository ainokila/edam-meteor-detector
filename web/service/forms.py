#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField, validators, DateField, PasswordField
from wtforms.validators import DataRequired

class ConfigCCDForm(FlaskForm):
    device_name = StringField('Device Name', render_kw={'readonly': True})
    exposition_time = DecimalField('Exposition Time', validators=[DataRequired()])
    gain = DecimalField('Gain', validators=[DataRequired()])

    start_time = DateField('Start time', format='%H:%M', validators=[DataRequired()])
    end_time = DateField('End time', format='%H:%M', validators=[DataRequired()])
    auto_start = BooleanField('Auto start')
    auto_config = BooleanField('Auto config')
    submit = SubmitField('Save Configuration')


class LoginForm(FlaskForm):
    username = StringField('Usename', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
