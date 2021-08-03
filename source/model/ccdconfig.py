#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

from source.utils.encoder import JSONCustomEncoder


class CCDConfig(object):

    def __init__(self, data={}):
        """Creates a new CCDConfig object

        Args:
            data (dict, optional): CCDConfig information. Defaults to {}.
        """
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


    def __repr__(self):
        return json.dumps(self.to_dict())

    def __hash__(self):
        return hash(tuple(self.__dict__.items()))

    def export_to_file(self, path):
        """ Exports CCD Config to a file

        Args:
            path (str):  Path where to save the CCD Config
        """
        with open(path, 'w') as client_conf_file:
            client_conf_file.write(json.dumps(
                self.to_dict(), cls=JSONCustomEncoder, indent=4, sort_keys=True))
            client_conf_file.close()


    @staticmethod
    def create_from_file(path):
        """ Creates an CCDConfig object using a config file

        Args:
            path (str): Path to load the configuration

        Returns:
            CCDConfig: CCDConfig object with the configuration
        """
        client_config = {}

        with open(path) as client_conf_file:
            client_config = json.load(client_conf_file)
            client_conf_file.close()

        return CCDConfig(data=client_config)
