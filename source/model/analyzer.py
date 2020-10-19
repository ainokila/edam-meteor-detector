#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from multiprocessing import Event, Process
from threading import Thread

from source.model.image.fits import ImageFits

# Check the following https://www.meteornews.net/2020/05/05/d64-nl-meteor-detecting-project/
# https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html


class ImageAnalyzer(Process):

    logger = logging.getLogger('ImageAnalyzer')

    def __init__(self, consumer_pipe):
        self.consumer = consumer_pipe
        self.stop = Event()
        self.previous_image = None
        super(ImageAnalyzer, self).__init__()

    def run(self):
        
        while not self.stop.is_set():
            if self.consumer.poll(15):
                filename = self.consumer.recv()
            else:
                continue

            image = ImageFits()
            image.load_data_from_file(filename)

            result = False
            # if self.previous_image:
            try:
                result = self.analyze_image(filename=filename, new_image=image)
            except Exception:
                pass

            if result:
                self.manage_posible(filename=filename)

            self.previous_image = image

    def analyze_image(self, filename, new_image):
        """ Analyzes an image searching possible meteors

        Args:
            new_image (ImageFits): Image fits to be analyzed

        Returns:
            boolean: returns True, if there is a possible meteor
        """
        lines = new_image.detect_lines()
        if lines:
            self.logger.info("Posible positive %s lines %s", filename, lines)
            return True
        else:
            self.logger.info("Discarding image %s lines %s", filename, lines)
            return False

    def manage_posible(self, filename):
        self.logger.info("Gestionando positivo")

    def stop_worker(self):
        self.stop.set()

