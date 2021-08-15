#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

from source.utils.encoder import JSONCustomEncoder


class BaseConfig(object):
  
    _CLASS = None

    def to_dict(self):
        raise NotImplementedError('Interface class')

    def _build_object(self, data):
        raise NotImplementedError('Interface class')

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __hash__(self):
        return hash(tuple(self.__dict__.items()))

    def export_to_file(self, path):
        """ Exports Config to a file

        Args:
            path (str):  Path where to save the Config
        """
        with open(path, 'w') as conf_file:
            conf_file.write(json.dumps(
                self.to_dict(), cls=JSONCustomEncoder, indent=4, sort_keys=True))
            conf_file.close()

    @classmethod
    def create_from_file(cls, path):
        """ Creates an Config object using a config file

        Args:
            path (str): Path to load the configuration

        Returns:
            _CLASS: Config object with the configuration
        """
        client_config = {}

        with open(path) as conf_file:
            client_config = json.load(conf_file)
            conf_file.close()

        return cls._CLASS(data=client_config)
