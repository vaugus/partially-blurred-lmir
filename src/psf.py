#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""psf.py."""

__version__ = '0.1'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

class PSF(object):

    def __init__(self, filename):
        self.filename = filename
        self.h = None
        self.H = None

    def __del__(self):
        del self

    def load_point_spread_function(self):
        self.h = scipy.ndimage.imread(self.filename, mode="L")
    
    def load_frequency_response_function(self):
        tmp_H = np.fft.fft2(self.h)
        
        # Identify the maximum value.
        max_freq = np.max(tmp_H)
        x, y = np.where(tmp_H == max_freq)

        # Work out the frequency at which H(u,v) becomes 0
        # for the first time after its maximum.

        # não sei o que é pra fazer aqui
        print (x)
        print (y) 

        self.H = tmp_H


    

# img = scipy.ndimage.imread('psf_binary_cropped_no_scale.jpg', mode='L')
# # img = imageio.imread('psf_binary_cropped_no_scale.jpg')

# img[img < 10] = 0
# img[img >= 10] = 1

# OTF = np.fft.fft2(img)

# otf_plot = np.abs(np.fft.fftshift(OTF))

# # plt.imshow(np.real(np.log2(OTF)), cmap="gray")
# # plt.imshow(np.real(OTF), cmap="gray")

# plt.imshow((np.abs(np.fft.fftshift(OTF))), cmap='gray')

# # plt.plot(otf_plot)

# plt.show()