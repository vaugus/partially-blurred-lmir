#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""psf.py."""

__version__ = '0.3'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

class PSF(object):
    """Class with operations concerning a PSF."""

    def __init__(self):
        """Constructor."""
        self.h = None
        self.H = None

    def __del__(self):
        """Destructor."""
        del self

    def load_point_spread_function(self, filename):
        """load_point_spread_function method.

        Loads the point spread function image in ndarray format.

        :param filename     The path to the point spread function image.
        """
        self.h = scipy.ndimage.imread(filename, mode="L")
    
    def load_frequency_response_function(self):
        """load_frequency_response_function method.

        Performs the 2D Fast Fourier Transform with the ndarray image object.
        """
        self.H = np.fft.fft2(self.h)
    