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


    def find_file(self, directory, name, extension=''):
        """Find the the file name in a directory

        Args:
            directory (str): Directory name
            name (str): Filename
            extension (str, optional): Extension filter. Defaults to ''.

        Returns:
            list: List with the file names
        """
        for _, _, files in os.walk(directory):
            for file in files:
                file_name = file.split('.')[-2]
                if file.endswith(extension) and name == file_name:
                    return file
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