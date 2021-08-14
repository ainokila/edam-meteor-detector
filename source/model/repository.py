#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from source.utils.variables import REPOSITORY_IMG_DATA_PATH


class ImageRepository(object):

    RAW = REPOSITORY_IMG_DATA_PATH + '/raw/'
    CANDIDATES = REPOSITORY_IMG_DATA_PATH + '/candidates/'
    DISCARDED = REPOSITORY_IMG_DATA_PATH + '/discarded/'
    POSITIVES = REPOSITORY_IMG_DATA_PATH + '/positives/'

    TYPE_MAPPING = {
        'candidates': CANDIDATES,
        'positives': POSITIVES,
        'discarded': DISCARDED,
        'raw': RAW,
    }

    def __init__(self):
        pass

    def list_files(self, img_type, extension=''):
        """Find the files name given an image type

        Args:
            img_type (str): Image type
            extension (str, optional): Extension filter. Defaults to ''.

        Returns:
            list: List with the file names
        """
        found_files = []
        for _, _, files in os.walk(self.TYPE_MAPPING[img_type]):
            for file in files:
                if file.endswith(extension):
                    found_files.append(file.split('.')[-2])
        return found_files


    def find_file(self, img_type, name, extension=''):
        """Find the the file name in a img_type

        Args:
            img_type (str): Image type
            name (str): Filename
            extension (str, optional): Extension filter. Defaults to ''.

        Returns:
            list: List with the file names
        """
        for _, _, files in os.walk(self.TYPE_MAPPING[img_type]):
            for file in files:
                file_name = file.split('.')[-2]
                if file.endswith(extension) and name == file_name:
                    return file_name
        return None

    def move_files(self, file_name, source, destination):
        """Move files ignoring the extension

        Args:
            file_name (str): Filename without extension
            source (str): Source path
            destination (str): Destination path
        """
        for _, _, files in os.walk(source):
            for file in files:
                if file.split('.')[-2] == file_name:
                    src_path_name = source + file
                    dst_path_name = destination + file
                    os.rename(src_path_name, dst_path_name)