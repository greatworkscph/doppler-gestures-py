# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>
# ryanvolz's Ambiguity Function](https://gist.github.com/ryanvolz/8b0d9f3e48ec8ddcef4d

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def ambiguity(code, nfreq=1):
    """Calculate the ambiguity function of code for nfreq frequencies.

    The ambiguity function is the square of the autocorrelation,
    normalized so the peak value is 1.

    For correct results, we require that nfreq >= len(code).

    The result is a 2-D array with the first index corresponding
    to frequency shift. The code is frequency shifted by
    normalized frequencies of range(nfreq)/nfreq and correlated
    with the baseband code. The result amb[0] gives the
    ambiguity with 0 frequency shift, amb[1] with 1/nfreq
    frequency shift, etc. These frequencies are the same as (and
    are in the same order as) the FFT frequencies for an nfreq-
    length FFT.
    ****Thus, the peak value is at amb[0, len(code) - 1]****

    To relocate the peak to the middle of the result, use
        np.fft.fftshift(amb, axes=0)
    To relocate the peak to the [0, 0] entry, use
        np.fft.ifftshift(amb, axes=1)

    """
    inlen = len(code)
    outlen = 2*inlen - 1
    #if nfreq < inlen:
    #    nfreq = inlen

    # Doppler shift the code to form a correlation bank in the form of a matrix
    doppleridx = np.arange(nfreq)[:, np.newaxis]*np.arange(inlen)
    dopplermat = np.exp(2*np.pi*1j*doppleridx/nfreq)
    # code is conjugated to form matched correlation
    codebank = code.conj()*dopplermat

    # initialize the output autocorrelation array
    acorr = np.zeros((nfreq, outlen), np.complex_)

    # correlate the Doppler-shifted codes with the original code
    # to get autocorrelation
    for k, shifted_code in enumerate(codebank):
        acorr[k] = np.correlate(code, shifted_code, mode='full')

    # calculate ambiguity function as normalized square magnitude of autocorrelation
    # (index of peak value is [0, inlen - 1])
    amb = np.abs(acorr / acorr[0, inlen - 1])**2

    return amb

def plotamb(code, channels, tone, window, rate):

    def update(frame_number):
        barker13 = np.asarray(code[0], np.complex)*mixer_sin
        b13amb = ambiguity(barker13, window)
        im.set_data(np.fft.fftshift(b13amb, axes=0).T)
        return im

    def init():
        barker13 = np.ones(L, np.complex)
        b13amb = ambiguity(barker13, window)
        im.set_data(a*np.fft.fftshift(b13amb, axes=0).T)
        return im

    fig = plt.figure()
    plt.xlabel('Frequency Index')
    plt.ylabel('Delay Index')

    barker13 = np.asarray(code[0], np.complex)
    L = len(barker13)
    b13amb = np.empty((window, 2*L-1), np.float)
    b13amb = ambiguity(barker13, window)
    if channels == 2:
        mixer_sin = np.array([(np.exp(2*np.pi*1j*tone*i/rate)) for i in range(L)])
    else:
        mixer_sin = np.array([(np.sin(2*np.pi*1 *tone*i/rate)) for i in range(L)])

    im = plt.imshow(
        np.fft.fftshift(b13amb, axes=0).T,
        extent=(0-window/2, 0+window/2, -L, L),
        aspect='auto', interpolation='none', origin='lower')

    anim = animation.FuncAnimation(fig, update, interval=50,)
    #anim = animation.FuncAnimation(fig, update, init_func=init, interval=50, blit=True,)

    plt.show()

    return 0
