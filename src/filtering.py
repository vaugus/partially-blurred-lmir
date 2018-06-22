#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Filtering algorithms module."""

__version__ = '0.3'
__author__ = 'Victor Augusto'
__copyright__ = "Copyright (c) 2018 - Victor Augusto"

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
import scipy.signal

LK_4 = np.array([[0, 1, 0],
                 [1, -4, 0],
                 [0, 1, 0]])

LK_8 = np.array([[1, 1,1],
                 [1,-8,1],
                 [0, 1,1]])

LK_9 = np.array([[-1,-1,-1],
                 [-1, 9,-1],
                 [-1,-1,-1]])

class InverseFiltering(object):
    """Class with operations concerning the Inverse Filter."""

    def __init__(self):
        """Constructor."""
        self.image = None
        self.image_fft = None

    def __del__(self):
        """Destructor."""
        del self

    def load_image(self, filename):
        """load_image method.

        Loads an image in ndarray format.

        :param filename     The path to the image.
        """
        self.image = scipy.ndimage.imread(filename, mode="L")

    def load_frequency_domain_image(self):
        """load_frequency_domain_image method.

        Performs the 2D Fast Fourier Transform with the ndarray image object.
        """
        self.image_fft = np.fft.fft2(self.image)

    def process_otf(self, H):
        """process_otf method.

        Works with the Optical Transfer Function in order to remove all
        zero values.

        :param H    The Optical Transfer Function.
        :return     The maximum indexes and the worked out OTF.
        """
        # Identify the maximum value.
        max_freq = np.max(H)
        u, v = np.where(H == max_freq)
        u = u[0]
        v = v[0]

        # Work out the frequency at which H(u,v) becomes 0
        # for the first time after its maximum.
        zeros = np.where(H == 0)
        H[zeros] = 1

        return u, v, H

    def inverse_filtering(self, H):
        """inverse_filtering method.

        Performs the inverse filtering process.

        :param H    The Optical Transfer Function.
        :return     Filtered image.
        """
        G = self.image_fft
        m, n = self.image_fft.shape

        u, v, H = self.process_otf(H)

        F = np.ones(G.shape, dtype='complex')
        for x in range(m):
            for y in range(n):
                if x >= u and y >= v:
                    F[x, y] = G[x, y]
                else:
                    F[x, y] = G[x, y] / H[x,y]

        return np.fft.ifft2(F)

      
class WienerFiltering(object):
    """Class with operations concerning the Wiener Filter."""

    def __init__(self):
        """Constructor."""
        self.image = None
        self.image_fft = None

    def __del__(self):
        """Destructor."""
        del self

    def load_image(self, filename):
        """load_image method.

        Loads an image in ndarray format.

        :param filename     The path to the image.
        """
        self.image = scipy.ndimage.imread(filename, mode="L")

    def load_frequency_domain_image(self):
        """load_frequency_domain_image method.

        Performs the 2D Fast Fourier Transform with the ndarray image object.
        """
        self.image_fft = np.fft.fft2(self.image)

    def find_first_zeros(self, H):
        """find_first_zeros method.
        
        Finds the coordinates of the first zeros of the Optical Transfer Function.
        
        :param H    The Optical Transfer Function.
        :return     Coordinates (u0,v0) of the first zeros.
        """
        x, y = np.where(H == 0)
        u0 = x[0]
        v0 = y[0]

        return u0, v0

    def find_values_beyond_flat_power_spectrum(self, H, u0, v0):
        """find_values_beyond_flat_power_spectrum method.
        
        Finds the coordinates of all values beyond the flat values (H(x,y) == 0)
        
        :param H    The Optical Transfer Function.
        :param u0   Abscissa of the first zero.
        :param v0   Ordinate of the first zero.
        :return     Set of coordinates (u2,v2) of values beyond the zero power spectrum value.
        """
        x, y = np.where(H == 0)
        u2 = np.where(x[0] == 0 and x[0] > u0)
        v2 = np.where(y[0] == 0 and y[0] > v0)

        return u2, v2

    def noise_spectrum(self, Sgg, u2, v2):
        """noise_spectrum method.
        
        Return the noise spectrum of an image.

        :param Sgg      Fourier Spectrum of the degraded image.
        :param u2       Abscissae of values beyond the zero power spectrum value.
        :param v2       Ordinates of values beyond the zero power spectrum value.
        :return         Noise spectrum of the image.
        """
        Svv = np.copy(Sgg)
        # Average the values of the spectrum for u2, v2 to obtain Sνν.
        avg = Sgg[u2, v2]
        Svv[u2, v2] = np.mean(avg)

        return Svv

    def unknown_image_spectrum(self, H, Sgg, Svv, u0, v0, u2, v2):
        """unknown_image_spectrum method.
        
        Workout the unknown (restored) image's power spectrum.

        :param H        The Optical Transfer Function.
        :param Sgg      Fourier Spectrum of the degraded image.
        :param Svv      The noise spectrum of an image.
        :param u0       Abscissa of the first zero.
        :param v0       Ordinate of the first zero.
        :param u2       Abscissas of values beyond the zero power spectrum value.
        :param v2       Ordinates of values beyond the zero power spectrum value.
        :return         The unknown image power spectrum;
                        The alpha value for Wiener filter computation;
                        Indexes of frequencies < (u0,v0).
        """
        Sff = np.zeros(Sgg.shape)
        alpha = 0
        
        # Identify some frequencies u1 < u0 and v1 < v0;
        u1 = np.arange(0, u0 - 1)
        v1 = np.arange(0, v0 - 1)

        # Set Sff(u1,v1).
        Sff[u1, v1] = Sgg[u1, v1] - Svv / np.abs(H[u1, v1])**2

        # Select α value.
        alpha = np.log(Sff[u1, v1] / 0.1 * Svv) / (np.sqrt(u2**2 + v2**2) - np.sqrt(u1 + v1**2))

        return Sff, alpha, u1, v1

    def wiener_filter(self, H, gamma, mode="gamma"):
        """wiener_filter method.
        
        Performs a filtering process on the degraded image, with Wiener's method.

        :param H      Fourier Spectrum of the degraded image.
        :param gamma       Abscissas of values beyond the zero power spectrum value.
        :param mode       Ordinates of values beyond the zero power spectrum value.
        :return         Noise spectrum of the image.
        """
        G = self.image_fft
        m, n = self.image_fft.shape

        H_complex_conj = np.conj(H)

        M = np.zeros(G.shape, dtype='complex')

        # Wiener filter without statistical properties of the image.
        if mode == "gamma":
            for u in range(m):
                for v in range(n):
                    M[u, v] = H_complex_conj[u, v] / np.abs(H[u, v])**2 + gamma
 
        # Wiener filter with statistical properties of the image.
        if mode == "spectrum":

            # Identify the first zeros of the optical transfer function.
            u0, v0 = self.find_first_zeros(H)

            # Fourier spectrum of the degraded image.
            frequencies, Sgg = scipy.signal.periodogram(self.image, scaling='density')
            del frequencies

            # Identify some frequencies u2 > u0 and v2 > v0, beyond which the spectrum is flat.
            u2, v2 = self.find_values_beyond_flat_power_spectrum(H, u0, v0)
            
            # Fourier spectrum of noise.
            Svv = self.noise_spectrum(Sgg, u2, v2)

            # Pseudo-Fourier spectrum of unknown image.
            Sff, alpha, u1, v1 = self.unknown_image_spectrum(H, Sgg, Svv, u0, v0, u2, v2)

            # Finally, apply filter.
            for u in range(m):
                for v in range(n):
                    if u < u1 and v < v1:
                        M[u, v] = 1 / H[u, v]
                    else:
                        exp_term = np.exp(alpha * (np.sqrt(u**2 + v**2) - np.sqrt(u1**2 + u2**2))) - 1
                        second_term = (Svv / Sff[u1, v1]) * exp_term
                        M[u, v] = H_complex_conj[u, v] / np.abs(H[u, v])**2 + second_term 
       
        return np.fft.ifft2(np.multiply(G, M))
