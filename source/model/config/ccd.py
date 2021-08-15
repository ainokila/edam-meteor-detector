#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.config.base_config import BaseConfig


class CCDConfig(BaseConfig):

    def __init__(self, data={}):
        """Creates a new CCDConfig object

        Args:
            data (dict, optional): CCDConfig information. Defaults to {}.
        """
        super(CCDConfig, self).__init__()
        self.device_name = None
        self.exposure_time = None
        self.gain = None
        self.start_time = None
        self.end_time = None
        self.auto_start = False
        self.auto_config = False
        self._build_object(data)

    def to_dict(self):
        """ Returns the information in a dictionary

        Returns:
            dict: CCDConfig information in a dict
        """
        conf = {
            'device_name': self.device_name,
            'exposition_time': self.exposure_time,
            'gain': self.gain,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'auto_start': self.auto_start,
            'auto_config': self.auto_config,
        }
        return conf

    def _build_object(self, data):
        """ Build the user information using a dictionary

        Args:
            data (dict): User information
        """
        self.device_name = data.get('device_name', None)
        self.exposure_time = data.get('exposition_time', None)
        self.gain = data.get('gain', None)
        self.start_time = data.get('start_time', '')
        self.end_time = data.get('end_time', '')
        self.auto_start = data.get('auto_start', False)
        self.auto_config = data.get('auto_config', False)

CCDConfig._CLASS = CCDConfig