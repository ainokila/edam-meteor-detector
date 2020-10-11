#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.model.user import User


class TestUserModel:

    def test_create_empty_user(self):
        user = User()

        assert user.username == None
        assert user.password == None

        user_dict = user.to_dict()

        assert user.username == user_dict['username']
        assert user.password == user_dict['password']

    def test_create_user(self):
        username = "myusername"
        pwd = "mypassword"
        user_info = {
            "username": username,
            "password": pwd
        }
        user = User(data=user_info)

        assert user.username == username
        assert user.password == pwd

        user_dict = user.to_dict()

        assert user.username == user_dict['username']
        assert user.password == user_dict['password']