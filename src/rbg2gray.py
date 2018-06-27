#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools module."""

__version__ = '1.0'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

def save_image(data, dpi, name):
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
    fig.savefig(str(name) + '_.png', dpi=dpi)

    plt.show()


for i in range(1,11):
    img = scipy.ndimage.imread(str(i) + '.jpg', mode='L')
    save_image(img, 100, i)
