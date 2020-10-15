#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Event, Process
from threading import Thread

from source.model.image.fits import ImageFits

# Check the following https://www.meteornews.net/2020/05/05/d64-nl-meteor-detecting-project/
# https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html


class ImageAnalyzer(Process):

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
            if self.previous_image:
                try:
                    result = self.analyze_image(new_image=image)
                except Exception:
                    pass

            if result:
                self.manage_posible(file_name=filename)

            self.previous_image = image

    def analyze_image(self, new_image):
        return True

    def manage_posible(self, file_name):
        pass

    def stop_worker(self):
        self.stop.set()

