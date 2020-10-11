#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class User(object):

    def __init__(self, data={}):
        """Creates a new User object

        Args:
            data (dict, optional): User information. Defaults to {}.
        """
        self.username = None
        self.password = None
        self._build_object(data)

    def to_dict(self):
        """ Returns the information in a dictionary

        Returns:
            dict: Username information in a dict
        """
        user = {
            'username': self.username,
            'password': self.password
        }
        return user

    def _build_object(self, data):
        """ Build the user information using a dictionary

        Args:
            data (dict): User information
        """
        self.username = data.get('username', None)
        self.password = data.get('password', None)
