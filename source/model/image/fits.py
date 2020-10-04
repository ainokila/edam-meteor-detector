#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.image.base import ImageBase
from astropy.io import fits

class ImageFits(ImageBase):

    def __init__(self):
        ImageBase.__init__(self)

    def load_data_from_file(self, path_file):
        file_data = self._read_file(path_file)
        self.load_data(file_data)

    def load_data(self, file_object):
        hdu_list = fits.open(file_object)
        self.data = hdu_list

    def save_image(self, path_file):
        raise NotImplementedError

    def diff(self, image):
        # a = fits.FITSDiff(self.data, image.data)
        # a.diff_hdus[0][1].diff_data.diff_pixels
        a = fits.ImageDataDiff(self.data[0], image.data[0])
        return a
