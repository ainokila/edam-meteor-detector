#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.config.base_config import BaseConfig


class NotificationConfig(BaseConfig):

    def __init__(self, data={}):
        """Creates a new NotificationConfig object

        Args:
            data (dict, optional): NotificationConfig information. Defaults to {}.
        """
        super(NotificationConfig, self).__init__()
        self.enabled_notifications = None
        self.telegram_api_id = None
        self.telegram_api_hash = None
        self.telegram_receivers = None
        self.check_hour = None
        self._build_object(data)

    def to_dict(self):
        """ Returns the information in a dictionary

        Returns:
            dict: NotificationConfig information in a dict
        """
        conf = {
            'enabled_notifications': self.enabled_notifications,
            'telegram_api_id': self.telegram_api_id,
            'telegram_api_hash': self.telegram_api_hash,
            'telegram_receivers': self.telegram_receivers,
            'check_hour': self.check_hour
        }
        return conf

    def _build_object(self, data):
        """ Build the user information using a dictionary

        Args:
            data (dict): User information
        """
        self.enabled_notifications = data.get('enabled_notifications', False)
        self.telegram_api_id = data.get('telegram_api_id', None)
        self.telegram_api_hash = data.get('telegram_api_hash', None)
        self.telegram_receivers = data.get('telegram_receivers', '')
        self.check_hour = data.get('check_hour', '08:00')

NotificationConfig._CLASS = NotificationConfig