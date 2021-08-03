#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import decimal
from datetime import time

class JSONCustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, time):
            return o.strftime("%H:%M")
        else:
            return super(JSONCustomEncoder, self).default(o)