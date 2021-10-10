#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from skimage.metrics import structural_similarity


class MeteorDetector(object):

    def __init__(self, image, mask):

        self.previous_image = None
        self.image = self._load_gray_image(image)
        self.mask = self._load_gray_image(mask)
        
    def update_img(self, image):
        """ Loads a new images and moves the previous

        Args:
            image (str): Image path
        """
        self.previous_image = self.image
        self.image = self._load_gray_image(image)

    def _load_gray_image(self, filename):
        """ Loads a image is a gray scale

        Args:
            filename (str): Image path

        Returns:
            numpy.ndarray: OpenCV image in gray scale
        """
        return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)

    def _subtract_images(self, img_1, img_2):
        """ Subtracts two images

        Args:
            img_1 (numpy.ndarray): Image 1
            img_2 (numpy.ndarray): Image 2

        Returns:
            numpy.ndarray: Subtracted image
        """
        return cv2.subtract(img_1, img_2)

    def _apply_mask(self, image):
        """ Applies the mask to the image

        Args:
            image (numpy.ndarray): Image where the mask will be applied

        Returns:
            numpy.ndarray: OpenCV image in gray scale with the mask applied
        """
        return self._subtract_images(image, self.mask)

    def _similarity_images(self, img_1, img_2):
        """ Generates a new image with the differences

        Args:
            img_1 (numpy.ndarray): Image 1
            img_2 (numpy.ndarray): Image 2

        Returns:
            numpy.ndarray: New image with the differences
        """
        (score, diff) = structural_similarity(img_1, img_2, full=True)
        return diff

    def calculate_lines(self):
        """ Calculates the lines in the current image

        Returns:
            numpy.ndarray: List with the lines
        """
        current_img_mask = self._apply_mask(self.image)

        if self.previous_image is not None:
            previous_img_mask = self._apply_mask(self.previous_image)

            diff = self._similarity_images(previous_img_mask, current_img_mask)
        else:
            diff = current_img_mask

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
                            
        return lines

    def has_meteor(self):
        """ Decides if the image could contain a meteor

        Returns:
            boolean: True if the image contains a meteor
        """
        result = self.calculate_lines()
        if isinstance(result, np.ndarray):
            return len(result) > 0
        else:
            return False



if __name__ == '__main__':

    image = '/home/ainokila/Escritorio/analisis_paso_3.png'

    import cv2 as cv
    import numpy as np

    img = cv.cvtColor(cv2.imread(image), cv2.COLOR_BGR2GRAY)

    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,50,150,apertureSize = 3)
    lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    cv.imwrite('houghlines5.jpg',img)