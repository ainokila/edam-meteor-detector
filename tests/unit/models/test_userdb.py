#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest
import string
import random

from source.model.user import User
from source.db.userdb import UserDB


class TestUserDB:

    DB_PATH = './userdbtest.db'

    @classmethod
    def _remove_file(cls, path):
        """ Remove a file from a path

        Args:
            path (str): File name
        """
        os.remove(path)

    @classmethod
    def setup_class(cls):
        cls.userdb = UserDB(db_path=cls.DB_PATH)

    @classmethod
    def teardown_class(cls):
        cls.userdb._close_db()
        cls._remove_file(cls.DB_PATH)

    def get_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_insert_user(self):
        username = self.get_random_string()
        password = self.get_random_string()
        user = User({'username': username, 'password': password})

        self.userdb.insert_user(user)

        assert self.userdb.db[username].username == user.username
        assert self.userdb.db[username].password == user.password

    def test_get_user(self):
        username = self.get_random_string()
        password = self.get_random_string()
        user = User({'username': username, 'password': password})

        self.userdb.insert_user(user)

        user = self.userdb.get_user(username)

        assert user.username == user.username
        assert user.password == user.password

        # Non exists
        fake = self.userdb.get_user(self.get_random_string())
        assert fake == None


    def test_update_user(self):
        username = self.get_random_string()
        password = self.get_random_string()
        user = User({'username': username, 'password': password})

        self.userdb.insert_user(user)

        user = self.userdb.get_user(username)

        assert user.username == user.username
        assert user.password == user.password

        user.password = self.get_random_string()
        self.userdb.update_user(user)

        user = self.userdb.get_user(username)

        assert user.username == user.username
        assert user.password == user.password

    def test_delete_user(self):
        username = self.get_random_string()
        password = self.get_random_string()
        user = User({'username': username, 'password': password})

        self.userdb.insert_user(user)

        self.userdb.delete_user(user)

        delete_user = self.userdb.get_user(username)
        assert delete_user == None