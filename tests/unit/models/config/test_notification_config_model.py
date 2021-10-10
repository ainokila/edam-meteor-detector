#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.model.config.notification import NotificationConfig


class TestNotificationConfigModel:

    def test_create_empty_notification_config(self):
        config = NotificationConfig()

        assert config.enabled_notifications == False
        assert config.telegram_api_id == None
        assert config.telegram_api_hash == None
        assert config.telegram_receivers == ''
        assert config.check_hour == '08:00'


    def test_create_notification_config(self):

        enabled_notifications = True
        telegram_api_id = '123445'
        telegram_api_hash = 'asdfadsfasd'
        telegram_receivers = '@myfake,@otherfake'
        check_hour = '08:00'

        config_info = {
            'enabled_notifications': enabled_notifications,
            'telegram_api_id': telegram_api_id,
            'telegram_api_hash': telegram_api_hash,
            'telegram_receivers': telegram_receivers,
            'check_hour': check_hour,
        }
        config = NotificationConfig(data=config_info)

        assert config.enabled_notifications == enabled_notifications
        assert config.telegram_api_id == telegram_api_id
        assert config.telegram_api_hash == telegram_api_hash
        assert config.telegram_receivers == telegram_receivers
        assert config.check_hour == check_hour



    def test_notification_config_to_dict(self):
        
        config_info = {
            'enabled_notifications': True,
            'telegram_api_id': 'telegram_api_id',
            'telegram_api_hash': 'telegram_api_hash',
            'telegram_receivers': 'telegram_receivers',
            'check_hour': 'check_hour',
        }
        config = NotificationConfig(data=config_info)
        assert config.to_dict()