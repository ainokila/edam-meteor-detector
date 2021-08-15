#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.model.config.analyzer import AnalyzerConfig


class TestAnalyzerConfigModel:

    def test_create_empty_analyzer_config(self):
        config = AnalyzerConfig()

        assert config.mask_path == None

    def test_create_analyzer_config(self):

        config_info = {
            'mask_path': 'test/dataa'
        }
        config = AnalyzerConfig(data=config_info)

        assert config.mask_path == 'test/dataa'


    def test_analyzer_config_to_dict(self):
        
        config_info = {
            'mask_path': 'test'
        }
        config = AnalyzerConfig(data=config_info)
        assert config.to_dict()