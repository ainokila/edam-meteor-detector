#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from multiprocessing import Event, Process
from threading import Thread

from source.model.image.fits import ImageFits

from source.utils.image.formats import _fits_to_jpg
from source.model.repository import ImageRepository


# Check the following https://www.meteornews.net/2020/05/05/d64-nl-meteor-detecting-project/
# https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html


class ImageAnalyzer(Process):

    logger = logging.getLogger('ImageAnalyzer')
    image_repository = ImageRepository()

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
            try:
                result = self.analyze_image(filename=filename, new_image=image)
            except Exception as e:
                print(e)

            image_name = self.export_to_jpg(filename, image)
            if result:
                self.move_images(image_name, ImageRepository.RAW, ImageRepository.CANDIDATES)
            else:
                self.move_images(image_name, ImageRepository.RAW, ImageRepository.DISCARDED)

    def analyze_image(self, filename, new_image):
        """ Analyzes an image searching possible meteors

        Args:
            new_image (ImageFits): Image fits to be analyzed

        Returns:
            boolean: returns True, if there is a possible meteor
        """
        return False

        lines = new_image.detect_lines()
        # lines = [1,3,4,5,6]
        if len(lines): # > umbral:
            self.logger.info("Posible positive %s lines %s", filename, len(lines))
            return True
        else:
            self.logger.info("Discarding image %s lines %s", filename, len(lines))
            return False

    def export_to_jpg(self, filename, new_image):
        """Save an image using jpg format

        Args:
            filename (str): File path
            new_image (ImageFits): ImageFits 

        Returns:
            str: File name without extension
        """
        image_name = filename.split('/')[-1].split('.')[-2]
        output_name_jpg = ImageRepository.RAW + image_name + '.jpg'
        _fits_to_jpg(new_image, output_name_jpg)
        return image_name

    def move_images(self, image_name, source, destination):
        """ Move the images from raw path to the destination

        Args:
            image_name (str): File name
            source (str): Source path
            destination (str): Destionation path
        """
        self.image_repository.move_files(image_name, source, destination)

    def stop_worker(self):
        self.stop.set()

