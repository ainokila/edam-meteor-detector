#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import cv2 as cv
import numpy as np

from astropy.io import fits

from source.model.image.base import ImageBase


class ImageFits(ImageBase):

    def __init__(self):
        ImageBase.__init__(self)

    def load_data_from_file(self, path_file):
        """ Load a fits image from a file

        Args:
            path_file (str): Image file
        """
        self.load_data(self._read_file(path_file))

    def load_data(self, file_object):
        """ Load a fits from a file object

        Args:
            file_object (FileObject): Python file object
        """
        self.data = fits.open(file_object)

    def load_from_array(self, array):
        self.data = fits.HDUList()
        self.data.append(fits.ImageHDU(data=array))

    def save_image(self, path_file):
        """ Save the fits in a path

        Args:
            path_file (str): Path name
        """
        self.data.writeto(path_file)

    def diff(self, image):
        """ Compare two fits and return a new ImageFits

        Args:
            image (ImageFits): Image to compare

        Returns:
            ImageFits: ImageFits with the differences
        """

        back_sub = cv.createBackgroundSubtractorMOG2()
        back_sub.apply(self.data[0].data)
        diff = back_sub.apply(image.data[0].data)

        diff_image = ImageFits()
        diff_image.load_from_array(diff)

        return diff_image

    def detect_lines(self, min_line=50, max_line_gap=5):
        """Apply the Hough algorithm to detect lines

        Args:
            min_line (int, optional): Line lenght. Defaults to 50.
            max_line_gap (int, optional): Line gap. Defaults to 5.

        Returns:
            list: Number of detected lines
        """
        image = self.data[0].data

        # Make a gray-scale copy and save the result in the variable 'gray'
        # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = image

        # Apply blur and save the result in the variable 'blur'
        blur = cv.GaussianBlur(gray, (5,5), 0)

        # Apply the Canny edge algorithm
        canny = cv.Canny(blur, 100, 200, 3)

        return cv.HoughLinesP(canny, 1, np.pi/180, 25, minLineLength=min_line, maxLineGap=max_line_gap)