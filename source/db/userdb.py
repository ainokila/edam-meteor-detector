#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shelve

class UserDB(object):

    DEFAULT_DB_PATH = './user.db'

    def __init__(self, db_path=None):

        if not db_path:
            db_path = self.DEFAULT_DB_PATH

        self.db = shelve.open(db_path)

    def insert_user(self, user):
        """ Insert a User in database

        Args:
            user (User): User model
        """
        if user.username in self.db:
            # Raise duplicate key error
            pass
        else:
            self.db[user.username] = user

    def get_user(self, username):
        """ Get a User from db

        Args:
            username (str): Username identifier

        Returns:
            [User]: User model
        """
        if username in self.db:
            return self.db[username]
        else:
            return None


    def update_user(self, user):
        """ Update a user in database

        Args:
            user (User): User model
        """
        self.db[user.username] = user

    def delete_user(self, user):
        """ Delete a username from database

        Args:
            user (User): User to be deleted
        """
        if user.username in self.db:
            del self.db[user.username]
        else:
            # Raise not found error
            pass

    def _close_db(self):
        """ Close the file
        """
        self.db.close() 