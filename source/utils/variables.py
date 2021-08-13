#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 

CLIENT_CONFIG_PATH = os.environ.get('CLIENT_CONFIG_PATH', './config/client.json')
ANALYZER_CONFIG_PATH = os.environ.get('ANALYZER_CONFIG_PATH', './config/analyzer.json')
REPOSITORY_IMG_DATA_PATH = os.environ.get('REPOSITORY_IMG_DATA_PATH', os.environ['PYTHONPATH'] + '/web/static/data')
WEB_CONFIG_PATH = os.environ.get('WEB_CONFIG_PATH', os.environ['PYTHONPATH'] + '/config/web.json')