#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField, validators, PasswordField
from wtforms.fields.html5 import TimeField, DateTimeLocalField
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

from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class ConfigAnalyzerForm(FlaskForm):

    mask_path = StringField('Mask Path', render_kw={'readonly': True})
    mask_file = FileField(validators=[FileRequired()])

    submit = SubmitField('Update configuration')


    def _to_dict(self):
        return {
            'mask_path': self.mask_path.data
        }

class SearchRepositoryForm(FlaskForm):

    start_date = DateTimeLocalField('Start Date', default=datetime.now() - timedelta(days=1), format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('End Date', default=datetime.now(), format='%Y-%m-%dT%H:%M')

    submit = SubmitField('Search')


class ConfigNotificationForm(FlaskForm):

    enabled_notifications = BooleanField('Service Status')

    telegram_api_id = StringField('Telegram ID', render_kw={'readonly': True})
    telegram_api_hash = StringField('Telegram HASH', render_kw={'readonly': True})
    telegram_receivers = StringField('Telegram Users', validators=[DataRequired()])

    check_hour = TimeField('Send time', validators=[DataRequired()])

    submit = SubmitField('Search')

    def _to_dict(self):
        return {
            'enabled_notifications': bool(self.enabled_notifications.data),
            'telegram_api_id': self.telegram_api_id.data,
            'telegram_api_hash': self.telegram_api_hash.data,
            'telegram_receivers': self.telegram_receivers.data,
            'check_hour': self.check_hour.data,
        }