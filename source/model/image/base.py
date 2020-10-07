#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ImageBase(object):
    
    def __init__(self):
        self.data = None

    def _read_file(self, path_file):
        open_file = open(path_file, 'rb')
        #open_file.close()
        return open_file

    def _save_file(self, path_file, content):
        open_file = open(path_file, 'wb')
        open_file.write(content)
        open_file.close()

    def load_data_from_file(self, path_file):
        raise NotImplementedError

    def load_data(self, file_object):
        raise NotImplementedError

    def save_image(self, path_file):
        raise NotImplementedError

    def diff(self, image):
        raise NotImplementedError

