#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField, validators, PasswordField
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired, InputRequired
from wtforms.validators import NumberRange

class ConfigCCDForm(FlaskForm):
    device_name = StringField('Device Name', render_kw={'readonly': True})
    exposition_time = DecimalField('Exposition Time',
                                   validators=[
                                       NumberRange(
                                           min=0, max=150, message='Exposition must be between 0.1-150'),
                                       InputRequired("Field required")])
    gain = DecimalField('Gain',
                        validators=[
                            NumberRange(min=0, max=150, message='Gain must be between 0-150'), DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    auto_start = BooleanField('Auto start')
    auto_config = BooleanField('Auto config')
    submit = SubmitField('Save Configuration')

    def _to_dict(self):
        return {
            'device_name': self.device_name.data,
            'exposition_time': float(self.exposition_time.data),
            'gain': float(self.gain.data),
            'start_time': self.start_time.data,
            'end_time': self.end_time.data,
            'auto_start': bool(self.auto_start.data),
            'auto_config': bool(self.auto_config.data),
        }


class LoginForm(FlaskForm):
    username = StringField('Usename', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
