#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.model.image.base import ImageBase
from astropy.io import fits

class ImageFits(ImageBase):

    def __init__(self):
        ImageBase.__init__(self)

    def load_data_from_file(self, path_file):
        file_data = open(path_file, 'rb')
        self.load_data(file_data)

    def load_data(self, file_object):
        hdu_list = fits.open(file_object)
        self.data = hdu_list[0].data
        hdu_list.close()

    def save_data(self, path_file):
        pass

    def __sub__(self, image):
        pass

    def __len__(self):
        pass