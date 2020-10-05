#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import numpy as np
import os
import filecmp

from astropy.io import fits
from astropy.io.fits.hdu.image import PrimaryHDU

from source.model.image.fits import ImageFits



class TestFitsModel:

    PATH_1 = './image1.fits'
    PATH_2 = './image2.fits'
    PATH_SAVE = './image_save.fits'

    HEIGHT = 100
    WIDTH = 100

    @classmethod
    def _create_fits_image(cls, path, value):
        """ Create a fake fits image

        Args:
            path str: Path file
            value int: Color value

        Returns:
            nparray: Numpy array with image values
        """
        data = np.full(shape=(cls.HEIGHT, cls.WIDTH), fill_value=value, dtype=np.float64)
        new_hdul = fits.HDUList()
        new_hdul.append(fits.ImageHDU(data=data))
        new_hdul.writeto(path)
        return data

    @classmethod
    def _remove_file(cls, path):
        """ Remove a file from a path

        Args:
            path (str): File name
        """
        os.remove(path)

    @classmethod
    def setup_class(cls):
        cls.image1 = cls._create_fits_image(cls.PATH_1, 0)
        cls.image2 = cls._create_fits_image(cls.PATH_2, 255)

    @classmethod
    def teardown_class(cls):
        cls._remove_file(cls.PATH_1)
        cls._remove_file(cls.PATH_2)
        cls._remove_file(cls.PATH_SAVE)

    def test_load_from_file(self):
        image = ImageFits()
        image.load_data_from_file(self.PATH_1)
    
        image2 = ImageFits()
        image2.load_data_from_file(self.PATH_2)

        assert len(image.data) == 1
        assert type(image.data[0]) == PrimaryHDU
        assert image.data[0].data.tolist() == self.image1.tolist()

        assert len(image2.data) == 1
        assert type(image2.data[0]) == PrimaryHDU
        assert image2.data[0].data.tolist() == self.image2.tolist()

    def test_load_from_file_object(self):
        open_file = open(self.PATH_1, 'rb')
        image = ImageFits()
        image.load_data(open_file)

        assert len(image.data) == 1
        assert type(image.data[0]) == PrimaryHDU
        assert image.data[0].data.tolist() == self.image1.tolist()

    def test_save_fits(self):
        open_file = open(self.PATH_1, 'rb')
        image = ImageFits()
        image.load_data(open_file)
        image.save_image(self.PATH_SAVE)
        assert filecmp.cmp(self.PATH_1, self.PATH_SAVE) 

    def test_diff(self):
        image = ImageFits()
        image.load_data_from_file(self.PATH_1)

        image2 = ImageFits()
        image2.load_data_from_file(self.PATH_2)

        equal = image.diff(image2)
        assert equal.diff_total == self.HEIGHT * self.WIDTH
        #assert equal.diff_pixels == 1
        #equal = image2.diff(image2)
        #assert len(equal.diff_pixels) == 0

    def test_diff_equal(self):
        image = ImageFits()
        image.load_data_from_file(self.PATH_1)

        equal = image.diff(image)
        assert len(equal.diff_pixels) == 0
        assert equal.diff_total == 0
