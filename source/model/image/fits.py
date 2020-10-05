#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.image.base import ImageBase
from astropy.io import fits

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
        

    def save_image(self, path_file):
        """ Save the fits in a path

        Args:
            path_file (str): Path name
        """
        self.data.writeto(path_file)

    def diff(self, image):
        """ Compare two fits using ImageDataDiff

        Args:
            image (ImageFits): Image to compare

        Returns:
            ImageDataDiff: ImageDataDiff with the differences
        """
        # a = fits.FITSDiff(self.data, image.data)
        # a.diff_hdus[0][1].diff_data.diff_pixels
        a = fits.ImageDataDiff(self.data[0].data, image.data[0].data)
        return a
