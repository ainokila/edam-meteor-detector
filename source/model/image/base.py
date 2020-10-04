#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ImageBase(object):
    
    def __init__(self):
        self.data = None

    def load_data_from_file(self, path_file):
        open_file = open(path_file,'rb')
        self.data = open_file.read()
        open_file.close()

    def load_data(self, data):
        self.data = data

    def save_data(self, path_file):
        open_file = open(path_file,'wb')
        open_file.write(self.data)
        open_file.close()

    def __sub__(self, image):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError
