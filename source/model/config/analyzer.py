#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.config.base_config import BaseConfig


class AnalyzerConfig(BaseConfig):
    
    def __init__(self, data={}):
        """Creates a new AnalyzerConfig object

        Args:
            data (dict, optional): AnalyzerConfig information. Defaults to {}.
        """
        super(AnalyzerConfig, self).__init__()
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

AnalyzerConfig._CLASS = AnalyzerConfig
