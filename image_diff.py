#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np

from source.model.image.fits import ImageFits

a = ImageFits()
a.load_data_from_file('data/image1.fits')
b = ImageFits()
b.load_data_from_file('data/image2.fits')

a.diff(b).save_image('data/diff.fits')
# print(diff.data[0].data)
# 
# cv2.imshow('Viewer', diff.data[0].data)
# # print(fits.HDUList(hdus=[fits.ImageHDU(data=backSub.apply(img2))])[0].data)
# # 
# if cv2.waitKey(2000) & 0xFF == ord('q'):
#     exit