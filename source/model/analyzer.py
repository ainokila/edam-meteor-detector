#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from multiprocessing import Event, Process
from threading import Thread

from source.model.image.fits import ImageFits

from source.utils.image.formats import _fits_to_jpg
from source.model.repository import ImageRepository
from source.analysis.meteor import MeteorDetector
from source.model.config.analyzer import AnalyzerConfig
from source.utils.variables import ANALYZER_CONFIG_PATH

class ImageAnalyzer(Process):

    logger = logging.getLogger('ImageAnalyzer')
    IMAGE_REPOSITORY = ImageRepository()
    SETTINGS_PATH = ANALYZER_CONFIG_PATH

    def __init__(self, consumer_pipe):
        self.consumer = consumer_pipe
        self.stop = Event()
        self.previous_image = None
        self.detector = None
        self.analyzer_conf = AnalyzerConfig.create_from_file(ANALYZER_CONFIG_PATH)
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
            image_name = self.export_to_jpg(filename, image)

            try:
                image_path = ImageRepository.RAW + image_name + '.jpg'
                if self.detector is None:
                    self.detector = MeteorDetector(image_path, self.analyzer_conf.mask_path)
                    self.logger.info('Initializing meteor detector')
                    continue
                else:
                    self.detector.update_img(image_path)

                result = self.detector.has_meteor()
            except Exception as e:
                self.logger.critical("Exception during analyze image", exc_info=True)


            if result:
                self.logger.info("DETECTION - Posible positive in %s", filename)
                self.generate_gif(image_name)
                self.move_images(image_name, ImageRepository.RAW, ImageRepository.CANDIDATES)
            else:
                self.logger.info("DETECTION - Discarding image %s", filename)
                self.move_images(image_name, ImageRepository.RAW, ImageRepository.DISCARDED)

    def generate_gif(self, image_name, number_images=2):
        """ Generates a GIF using the previos N images.

        Args:
            image_name (str): Image idenfifier
            number_images (int): Number of images to include in the gif
        """
        self.logger.info("Generating gif for %s", image_name)
        pass

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
        self.IMAGE_REPOSITORY.move_files(image_name, source, destination)

    def stop_worker(self):
        self.stop.set()

