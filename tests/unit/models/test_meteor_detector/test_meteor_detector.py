#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os 
import numpy as np
from source.analysis.meteor import MeteorDetector


class TestMeteorDetector:

    IMG_BLACK = 'tests/unit/models/test_meteor_detector/imgs/black.jpg'
    IMG_WHITE = 'tests/unit/models/test_meteor_detector/imgs/white.jpg'
    IMG_MASK = 'tests/unit/models/test_meteor_detector/imgs/mask.png'


    def test_analyze_without_previous_img(self):
        detector = MeteorDetector(self.IMG_BLACK, self.IMG_MASK)
        assert detector.calculate_lines() == None
        assert detector.has_meteor() == False, 'Detected a positive, incorrect detection'


    def test_analyze_positive(self):
        detector = MeteorDetector(self.IMG_BLACK, self.IMG_MASK)
        detector.update_img(self.IMG_WHITE)
        lines = detector.calculate_lines()
        assert isinstance(lines, np.ndarray), 'Incorrect type returned by calculate_lines'
        assert detector.has_meteor() == True, 'No detected a positive, incorrect detection'

        detector.update_img(self.IMG_BLACK)
        lines = detector.calculate_lines()
        assert isinstance(lines, np.ndarray), 'Incorrect type returned by calculate_lines'
        assert detector.has_meteor() == True, 'No detected a positive, incorrect detection'
