#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from PIL import Image
from astropy.io import fits
import math


def _sqrt(inputArray, scale_min=None, scale_max=None):
	imageData=np.array(inputArray, copy=True)
	if scale_min == None:
		scale_min = imageData.min()
	if scale_max == None:
		scale_max = imageData.max()
	imageData = imageData.clip(min=scale_min, max=scale_max)
	imageData = imageData - scale_min
	indices = np.where(imageData < 0)
	imageData[indices] = 0.0
	imageData = np.sqrt(imageData)
	imageData = imageData / math.sqrt(scale_max - scale_min)
	return imageData


def _fits_to_jpg(image_data, file_path):
    """ Exports a image data as jpg file

    Args:
        image_data (F): [description]
        file_path ([type]): [description]
    """
    image_data = image_data.data[0].data
    if len(image_data.shape) == 2:
        sum_image = image_data
    else:
        sum_image = image_data[0] - image_data[0]
        for single_image_data in image_data:
            sum_image += single_image_data  

    sum_image = _sqrt(sum_image, scale_min=0, scale_max=np.amax(image_data))
    sum_image = sum_image * 200
    im = Image.fromarray((sum_image).astype(np.uint8))
    if im.mode != 'RGB':
        im = im.convert('RGB')

    im.save(file_path)
    im.close()