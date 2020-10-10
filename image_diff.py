#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np

from source.model.image.fits import ImageFits

a = ImageFits()
a.load_data_from_file('data/image1.fits')
b = ImageFits()
b.load_data_from_file('data/image2.fits')

# a.diff(b).save_image('data/diff.fits')
# print(diff.data[0].data)
# 

# Aplicar suavizado Gaussiano
img = a.diff(b).data[0].data

gauss = cv2.GaussianBlur(img, (5,5), 0)
 
canny = cv2.Canny(gauss, 50, 150)

# Buscamos los contornos
(contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Mostramos el número de monedas por consola
print("He encontrado {} objetos".format(len(contornos)))


cv2.imshow('Viewer', canny)
# # print(fits.HDUList(hdus=[fits.ImageHDU(data=backSub.apply(img2))])[0].data)
 
if cv2.waitKey(20000) & 0xFF == ord('q'):
    exit