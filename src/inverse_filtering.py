#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inverse_filtering.py."""

__version__ = '0.1'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

class InverseFiltering(object):

    def __init__(self, filename):
        self.filename = filename
        self.g = None
        self.G = None

    def __del__(self):
        del self

    def load_image(self):
        self.g = scipy.ndimage.imread(self.filename, mode="L")

    def load_frequency_domain_image(self):
        self.G = np.fft.fft2(self.g)

    def inverse_filtering(self):
        pass
        
