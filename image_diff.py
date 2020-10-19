#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 as cv
import math
import numpy as np

from source.model.image.fits import ImageFits

a = ImageFits()
a.load_data_from_file('web/static/data/raw/image1.fits')
b = ImageFits()
b.load_data_from_file('web/static/data/raw/image2.fits')

# a.diff(b).save_image('data/diff.fits')
# print(diff.data[0].data)
# 

new = a.diff(b)

image = new.data[0].data

# # Make a gray-scale copy and save the result in the variable 'gray'
# gray = image #cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# 
# # Apply blur and save the result in the variable 'blur'
# blur = cv.GaussianBlur(gray, (5,5), 0)
# 
# # Apply the Canny edge algorithm
# canny = cv.Canny(blur, 100, 200, 3)

# lines = cv.HoughLinesP(canny, 1, np.pi/180, 25, minLineLength=50, maxLineGap=5)

lines = new.detect_lines(min_line=10, max_line_gap=5)

print(len(lines))

if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(image, pt1, pt2, (0,0,255), 3, cv.LINE_AA)

cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", image)

cv.waitKey()

# Aplicar suavizado Gaussiano
# img = a.diff(b).data[0].data
# 
# gauss = cv2.GaussianBlur(img, (5,5), 0)
#  
# canny = cv2.Canny(gauss, 50, 150)
# 
# # Buscamos los contornos
# (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 
# # Mostramos el número de monedas por consola
# print("He encontrado {} objetos".format(len(contornos)))
# 
# 
# cv2.imshow('Viewer', canny)
# # # print(fits.HDUList(hdus=[fits.ImageHDU(data=backSub.apply(img2))])[0].data)
#  
# if cv2.waitKey(20000) & 0xFF == ord('q'):
#     exit