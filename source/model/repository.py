#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# ENV configuration
STATIC_PATH = os.environ['PYTHONPATH'] + '/web/static'
RAW = STATIC_PATH + '/data/raw/'
CANDIDATES = STATIC_PATH + '/data/candidates/'
DISCARDED = STATIC_PATH + '/data/discarded/'
POSITIVES = STATIC_PATH + '/data/positives/'


class ImageRepository(object):

    RAW = RAW
    CANDIDATES = CANDIDATES
    DISCARDED = DISCARDED
    POSITIVES = POSITIVES

    def __init__(self):
        pass

    def list_files(self, directory, extension=''):
        """Find the files name in a directory

        Args:
            directory (str): Directory name
            extension (str, optional): Extension filter. Defaults to ''.

        Returns:
            list: List with the file names
        """
        found_files = []
        for _, _, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    found_files.append(file)
        return found_files

    def move_file(self, file_name, source, destination):
        """[summary]

        Args:
            file_name ([type]): [description]
            source ([type]): [description]
            destination ([type]): [description]
        """
        src_path_name = source + file_name
        dst_path_name = destination + file_name
        os.rename(src_path_name, dst_path_name)