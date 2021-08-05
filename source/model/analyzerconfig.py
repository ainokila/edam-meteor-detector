#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

from source.utils.encoder import JSONCustomEncoder


class AnalyzerConfig(object):

    def __init__(self, data={}):
        """Creates a new AnalyzerConfig object

        Args:
            data (dict, optional): AnalyzerConfig information. Defaults to {}.
        """
        self.mask_path = None
        self._build_object(data)

    def to_dict(self):
        """ Returns the information in a dictionary

        Returns:
            dict: AnalyzerConfig information in a dict
        """
        conf = {
            'mask_path': self.mask_path
        }
        return conf

    def _build_object(self, data):
        """ Build the user information using a dictionary

        Args:
            data (dict): User information
        """
        self.mask_path = data.get('mask_path', None)


    def __repr__(self):
        return json.dumps(self.to_dict())

    def __hash__(self):
        return hash(tuple(self.__dict__.items()))

    def export_to_file(self, path):
        """ Exports AnalyzerConfig to a file

        Args:
            path (str):  Path where to save the AnalyzerConfig
        """
        with open(path, 'w') as client_conf_file:
            client_conf_file.write(json.dumps(
                self.to_dict(), cls=JSONCustomEncoder, indent=4, sort_keys=True))
            client_conf_file.close()

    @staticmethod
    def create_from_file(path):
        """ Creates an AnalyzerConfig object using a config file

        Args:
            path (str): Path to load the configuration

        Returns:
            AnalyzerConfig: AnalyzerConfig object with the configuration
        """
        client_config = {}

        with open(path) as client_conf_file:
            client_config = json.load(client_conf_file)
            client_conf_file.close()

        return AnalyzerConfig(data=client_config)
