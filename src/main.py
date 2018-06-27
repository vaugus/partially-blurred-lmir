#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""main.py file."""

__version__ = '1.0'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

from tools import Tools
from point_spread_function import PSF
from filtering import InverseFiltering
from filtering import WienerFiltering
from filtering import LK_9

import time
import numpy as np
import scipy.ndimage
from skimage import restoration


def main():
    # Initialization.
    psf = PSF()
    psf.load_point_spread_function('../input/psf/psf.jpg')
    psf.load_frequency_response_function()

    tools = Tools()

    method = int(input())
    original = str(input()).rstrip()
    optimal = str(input()).rstrip()

    opt = scipy.ndimage.imread(optimal, mode='L')

    start = time.time()

    if method == 1:
        inverse_filtering = InverseFiltering()
        inverse_filtering.load_image(original)
        inverse_filtering.load_frequency_domain_image()

        f = inverse_filtering.inverse_filtering(psf.H)
        g = inverse_filtering.image

    if method == 2:
        gamma = float(input())
        wiener_filtering = WienerFiltering()
        wiener_filtering.load_image(original)
        wiener_filtering.load_frequency_domain_image()

        f = wiener_filtering.wiener_filter(psf.H, gamma)
        g = wiener_filtering.image

    if method == 3:
        wiener_filtering = WienerFiltering()
        wiener_filtering.load_image(original)
        wiener_filtering.load_frequency_domain_image()

        f = wiener_filtering.wiener_filter(psf.H, 0, mode='spectrum')
        g = wiener_filtering.image

    if method == 4:
        g = scipy.ndimage.imread(original, mode='L')
        f = restoration.wiener(g, psf.h, 1)

    if method == 5:
        g = scipy.ndimage.imread(original, mode='L')
        f = restoration.richardson_lucy(g, psf.h, iterations=15)

    if method == 6:
        g = scipy.ndimage.imread(original, mode='L')
        f = scipy.signal.convolve2d(g, LK_9, mode='fill', boundary='wrap')        
    
    end = time.time()

    rmse_g = tools.rmse(opt, g, 'Optimal', 'Degraded')
    rmse_f = tools.rmse(opt, f, 'Optimal', 'Restored')

    tools.psnr(rmse_g, 'Optimal', 'Degraded')
    tools.psnr(rmse_f, 'Optimal', 'Restored')

    print (str(end - start))
    
if __name__ == "__main__":
    main()
    