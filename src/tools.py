#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools module."""

__version__ = '0.2'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

class Tools(object):
    """Class with tools for image processing and visualization operations."""

    def __init__(self):
        """Constructor."""

    def __del__(self):
        """Destructor."""
        del self

    def save_image(self, data, dpi=100):
        """save_image method.

        Saves the ndarray object as a png file.

        :param data     Image to be saved in a png format file.
        :param dpi      Amount of dots per inch, the printing resolution.
        """
        
        # Get the ndarray shape and set the amount of inches in the matplotlib figure.
        shape = np.shape(data)[0:2][::-1]
        size = [ float(i) / dpi for i in shape]

        fig = plt.figure()
        fig.set_size_inches(size)
        ax = plt.Axes(fig,[0,0,1,1])

        # Do not print the default matplotlib axis.
        ax.set_axis_off()
        fig.add_axes(ax)

        plt.imshow(data, cmap="gray")

        # Save it as a png file.
        fig.savefig('out.png', dpi=dpi)

        plt.show()

    def rmse(self, img1, img2):
        """rmse method.

        Calculates the root mean squared error between the ground truth image
        and the restored one.
        
        :param img1     Original image (ndarray).
        :param img2     Processed image (ndarray).
        """
        ans = np.sqrt(np.linalg.norm(img1 - img2) * (1 / img2.size))

        print ('RMSE: ' + '{:.4f}'.format(ans))

    def show_image(self, image, plot='default', dpi=100):
        """show_image method.

        Shows an image on the matplotlib plot frame, according to the image 
        properties.

        :param image    The image file to be shown.
        :param plot     The image origin, either a standard image or the result of a
                        operation concerning fft results.
        :param dpi      DPI for printing.
        """
        shape = np.shape(image)[0:2][::-1]
        size = [ float(i) / dpi for i in shape]

        fig = plt.figure()
        fig.set_size_inches(size)
        ax = plt.Axes(fig,[0,0,1,1])

        # Do not print those default matplotlib axes.
        ax.set_axis_off()
        fig.add_axes(ax)

        if plot == 'default':
            plt.imshow(image, cmap="gray")

        if plot == 'from_fft':
            plt.imshow(np.abs(image), cmap="gray")

        plt.show()


    def rgb2hsv(self, img):
        return colors.rgb_to_hsv(img)

