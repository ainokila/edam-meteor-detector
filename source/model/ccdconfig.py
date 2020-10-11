#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CCDConfig(object):

    def __init__(self, data={}):
        """Creates a new CCDConfig object

        Args:
            data (dict, optional): CCDConfig information. Defaults to {}.
        """
        self.device_name = None
        self.exposure_time = None
        self.gain = None
        self._build_object(data)

    def to_dict(self):
        """ Returns the information in a dictionary

        Returns:
            dict: CCDConfig information in a dict
        """
        conf = {
            'device_name': self.device_name,
            'exposure_time': self.exposure_time,
            'gain': self.gain,
        }
        return conf

    def _build_object(self, data):
        """ Build the user information using a dictionary

        Args:
            data (dict): User information
        """
        self.device_name = data.get('device_name', None)
        self.exposure_time = data.get('exposure_time', None)
        self.gain = data.get('gain', None)
