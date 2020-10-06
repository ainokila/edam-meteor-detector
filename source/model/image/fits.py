#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
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

        back_sub = cv2.createBackgroundSubtractorMOG2()
        back_sub.apply(self.data[0].data)
        diff = back_sub.apply(image.data[0].data)

        diff_image = ImageFits()
        diff_image.load_from_array(diff)

        return diff_image
