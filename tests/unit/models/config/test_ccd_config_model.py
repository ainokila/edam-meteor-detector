#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.model.config.ccd import CCDConfig


class TestCCDConfigModel:

    def test_create_empty_ccdconfig(self):
        config = CCDConfig()

        assert config.device_name == None
        assert config.exposure_time == None
        assert config.gain == None
        assert config.start_time == ''
        assert config.end_time == ''
        assert config.auto_start == False
        assert config.auto_config == False

    def test_create_ccdconfig(self):
        device_name = "device_name"
        exposure_time = 60
        gain = 60
        start_time = '20:00'
        end_time = '08:00'
        config_info = {
            'device_name': device_name,
            'exposition_time': exposure_time,
            'gain': gain,
            'start_time': start_time,
            'end_time': end_time,
            'auto_start': True,
            'auto_config': True,
        }
        config = CCDConfig(data=config_info)

        assert config.device_name == device_name
        assert config.exposure_time == exposure_time
        assert config.gain == gain
        assert config.start_time == start_time
        assert config.end_time == end_time
        assert config.auto_start == True
        assert config.auto_config == True

    def test_ccdconfig_to_dict(self):
        
        config_info = {
            'device_name': 'test',
            'exposition_time': 1,
            'gain': 1,
            'start_time': 'hh:ss',
            'end_time': 'hh:ss',
            'auto_start': True,
            'auto_config': True,
        }
        config = CCDConfig(data=config_info)
        assert config.to_dict()