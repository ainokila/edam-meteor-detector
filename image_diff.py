#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from skimage.metrics import structural_similarity
import cv2
import numpy as np

MASK = '/home/ainokila/Escritorio/imgs/test/mask_2.png'
IMG_1 = '/home/ainokila/Escritorio/imgs/test/normal.jpg'
IMG_2 = '/home/ainokila/Escritorio/imgs/test/white.jpg'


def lines_detector(img_1, img_2, img_filter, ui_view=False):

    mask = cv2.imread(img_filter)
    before = cv2.imread(img_1)
    after = cv2.imread(img_2)

    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    before_1 = cv2.subtract(before_gray, mask_gray)
    after_1 = cv2.subtract(after_gray, mask_gray)

    import pdb; pdb.set_trace()

    (score, diff) = structural_similarity(before_1, after_1, full=True)
    #score = 0
    #diff = cv2.subtract(before_1, after_1)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1] 
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(diff,(kernel_size, kernel_size),0)

    low_threshold = 1
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(diff) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    print(lines)

    if ui_view:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),2)
        
        # Draw the lines on the  image
        lines_edges = cv2.addWeighted(diff, 0.8, line_image, 1, 0)

        # cv2.imshow("mask_gray",mask_gray)
        cv2.imshow("diff", diff)
        cv2.imshow("detected lines", line_image)
        cv2.waitKey(0)

    return score, lines



print(lines_detector(IMG_1, IMG_2, MASK, ui_view=True))