#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.model.ccdconfig import CCDConfig


class TestCCDConfigModel:

    def test_create_empty_ccdconfig(self):
        config = CCDConfig()

        assert config.device_name == None
        assert config.exposure_time == None
        assert config.gain == None

        config_dict = config.to_dict()

        assert config.device_name == config_dict['device_name']
        assert config.exposure_time == config_dict['exposure_time']
        assert config.gain == config_dict['gain']

    def test_create_ccdconfig(self):
        device_name = "device_name"
        exposure_time = 60
        gain = 60
        config_info = {
            "device_name": device_name,
            "exposure_time": exposure_time,
            "gain": gain,
        }
        config = CCDConfig(data=config_info)

        assert config.device_name == device_name
        assert config.exposure_time == exposure_time
        assert config.gain == gain

        config_dict = config.to_dict()

        assert config.device_name == config_dict['device_name']
        assert config.exposure_time == config_dict['exposure_time']
        assert config.gain == config_dict['gain']