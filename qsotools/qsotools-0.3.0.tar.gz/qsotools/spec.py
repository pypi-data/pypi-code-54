""" Contains an object to describe a spectrum, and various
spectrum-related functions."""
from __future__ import division
import copy
import os, pdb
from math import sqrt
from pprint import pformat
import numpy as np
import matplotlib.pyplot as pl

c_kms = 2.99792458e5        # speed of light [km/s]

class Spectrum(object):
    """ A class to hold information about a spectrum.
    
    Attributes
    ----------
    wa : array of floats, shape(N,)
      Wavelength values (overrides all wavelength keywords)
    fl : array of floats, shape(N,)
      Flux.
    er : array of floats, shape(N,)
      Error.
    co : array of floats, shape(N,)
      Continuum.
    dw : float
      Wavelength difference between adjacent pixel centres.
    dv : float
      Velocity difference (km/s)
    fwhm : float
      Instrumental FWHM in km/s
    filename : str
      Filename of spectrum

    Notes
    -----
    If enough information is given, the wavelength scale will be
    generated.  Note that there is no error check if you give
    conflicting wavelength scale information in the keywords!  In this
    case certain combinations of keywords take precendence.  See the
    code comments for details.

    Notes for FITS header::
    
     wstart = CRVAL - (CRPIX - 1.0) * CDELT,  dw = CDELT

    Conversion between velocity width and log-linear pixel width::
    
     dv / c_kms = 1 - 10**(-dw)


    Examples
    --------
    >>> sp = Spectrum(wstart=4000, dw=1, npts=500)
    >>> sp = Spectrum(wstart=4000, dv=60, npts=500)
    >>> sp = Spectrum(wstart=4000, wend=4400, npts=500)
    >>> wa = np.linspace(4000, 5000, 500)
    >>> fl = np.ones(len(wa))
    >>> sp = Spectrum(wa=wa, fl=fl)
    >>> sp = Spectrum(CRVAL=4000, CRPIX=1, CDELT=1, fl=np.ones(500))
    """
    def __init__(self,
                 dw=None, dv=None, wstart=None, wend=None, npts=None,
                 CRVAL=None, CRPIX=None, CDELT=None,
                 wa=None, fl=None, er=None, co=None,
                 fwhm=None, filename=None):
        """ Create the wavelength scale and initialise attributes."""
        if fl is not None:
            fl = np.asarray(fl)
            fl[np.isinf(fl)] = np.nan
            self.fl = fl
            npts = len(fl)
        if er is not None:
            er = np.asarray(er)
            # replace bad values with NaN
            er[np.isinf(er)|(er<=0.)] = np.nan
            self.er = er
            npts = len(er)
        if co is not None:
            co = np.asarray(co)
            co[np.isinf(co)] = np.nan
            self.co = co
            npts = len(co)

        # Check whether we need to make a wavelength scale.
        makescale = True

        if dv is not None:
            dw = np.log10(1. / (1. - dv / c_kms))

        if None not in (CRVAL, CRPIX, CDELT) :
            wstart = CRVAL - (CRPIX - 1.0) * CDELT
            dw = CDELT
            # check if it's log-linear scale (heuristic)
            if CRVAL < 10:
                wstart = 10**wstart
                dv = c_kms * (1. - 1. / 10. ** -dw)

        if wa is not None:
            wa = np.asarray(wa, float)
            npts = len(wa)
            makescale = False
        elif None not in (wstart, dw, npts):
            if dv is not None:
                wstart = np.log10(wstart)
        elif None not in (wstart, wend, dw):
            if dv is not None:
                wstart, wend = np.log10([wstart,wend])
            # make sure the scale is the same or bigger than the
            # requested wavelength range
            npts = int(np.ceil((wend - wstart) / float(dw)))
        elif None not in (wstart, wend, npts):
            # Make a linear wavelength scale
            dw = (wend - wstart) / (npts - 1.0)
        elif None not in (wend, dw, npts):
            raise ValueError('Please specify wstart instead of wend')
        else:
            raise ValueError('Not enough info to make a wavelength scale!')

        if makescale:
            if debug: print('making wav scale,', wstart, dw, npts, bool(dv))
            wa = make_wa_scale(wstart, dw, npts, constantdv=bool(dv))
        else:
            # check whether wavelength scale is linear or log-linear
            # (constant velocity)
            diff = wa[1:] - wa[:-1]
            if np.allclose(diff, diff[0]):
                dw = np.median(diff)
            else:
                diff = np.log10(wa[1:]) - np.log10(wa[:-1])
                if np.allclose(diff, diff[0]):
                    dw = np.median(diff)
                    dv = c_kms * (1. - 1. / 10. ** dw)

        # assign remaining attributes
        if fl is None:
            self.fl = np.zeros(npts)
        if er is None:
            self.er = np.empty(npts) * np.nan  # error (one sig)
        if co is None:
            self.co = np.empty(npts) * np.nan

        self.fwhm = fwhm
        self.dw = dw
        self.dv = dv
        self.filename = filename
        self.wa = wa

    def __repr__(self):
        return 'Spectrum(wa, fl, er, co, dw, dv, fwhm, filename)'

    def multiply(self, val):
        """ Multipy the flux, error and continuum by `val`.
        
        >>> sp = Spectrum(wstart=4000, dw=1, npts=500, fl=np.ones(500))
        >>> sp.multiply(2)
        """
        self.fl *= val
        self.er *= val
        self.co *= val

    def plot(self, ax=None, show=True, yperc=0.98, alpha=0.8,
             linewidth=1., linestyle='steps-mid',
             flcolor='blue', cocolor='red'):
        """ Plots a spectrum.

        Returns the matplotlib artists that represent the flux, error
        and continuum curves.        
        """
        f,e,c,w = self.fl, self.er, self.co, self.wa
        return plot(w, f, e, c, ax=ax, show=show, yperc=yperc, alpha=alpha,
                    linewidth=linewidth, linestyle=linestyle,
                    flcolor=flcolor, cocolor=cocolor)

    def stats(self, wa1, wa2, show=False):
        """Calculates statistics (mean, standard deviation (i.e. RMS), mean
        error, etc) of the flux between two wavelength points.

        Returns::
        
         mean flux, RMS of flux, mean error, SNR:
            SNR = (mean flux / RMS)
        """
        i,j = self.wa.searchsorted([wa1, wa2])
        fl = self.fl[i:j]
        er = self.er[i:j]
        good = (er > 0) & ~np.isnan(fl)
        if len(good.nonzero()[0]) == 0:
            print('No good data in this range!')
            return np.nan, np.nan, np.nan, np.nan
        fl = fl[good]
        er = er[good]
        mfl = fl.mean()
        std = fl.std()
        mer = er.mean()
        snr = mfl / std
        if show:
            print('mean %g, std %g, er %g, snr %g' % (mfl, std, mer, snr))
        return mfl, std, mer, snr

    def rebin(self, **kwargs):
        """ Class method version of spec.rebin() """
        return rebin(self.wa, self.fl, self.er, **kwargs)

    def rebin_simple(self, n):
        """ Class method version of spec.rebin_simple()."""
        return rebin_simple(self.wa, self.fl, self.er, self.co, n)
    
    def write(self, filename, header=None, overwrite=False):
        """ Writes out a spectrum, as ascii - wavelength, flux, error,
        continuum.

        `overwrite` can be True or False.

        `header` is a string to be written to the file before the
        spectrum. A special case is `header='RESVEL'`, which means the
        instrumental fwhm in km/s will be written on the first line
        (VPFIT style).
        """
        if os.path.lexists(filename) and not overwrite:
            c = raw_input('File %s exists - overwrite? (y) or n: ' % filename)
            if c != '':
                if c.strip().lower()[0] == 'n':
                    print('returning without writing anything...')
                    return
        fh = open(filename, 'w')
        if header is not None:
            if header == 'RESVEL':
                if self.fwhm is None:
                    raise ValueError('Instrumental fwhm is not set!')
                fh.write('RESVEL %.2f' % self.fwhm)
            else:
                fh.write(header)
        fl = np.nan_to_num(self.fl)
        er = np.nan_to_num(self.er)
        if np.all(np.isnan(self.co)):
            for w,f,e in zip(self.wa, fl, er):
                fh.write("% .12g % #12.8g % #12.8g\n" % (w,f,e))
        else:
            co = np.nan_to_num(self.co)
            for w,f,e,c in zip(self.wa, fl, er, co):
                fh.write("% .12g % #12.8g % #12.8g % #12.8g\n" % (w,f,e,c))
        fh.close()
        if self.filename is None:
            self.filename = filename

def find_wa_edges(wa):
    """ Given wavelength bin centres, find the edges of wavelengh
    bins.

    Examples
    --------

    >>> print find_wa_edges([1, 2.1, 3.3, 4.6])
    [ 0.45  1.55  2.7   3.95  5.25]
    """
    wa = np.asarray(wa)
    edges = wa[:-1] + 0.5 * (wa[1:] - wa[:-1])
    edges = [2*wa[0] - edges[0]] + edges.tolist() + [2*wa[-1] - edges[-1]]
    return np.array(edges)
            
def rebin(wav, fl, er, **kwargs):
    """ Rebins spectrum to a new wavelength scale generated using the
    keyword parameters.

    Returns the rebinned spectrum.

    Accepts the same keywords as Spectrum.__init__() (see that
    docstring for a description of those keywords)

    Will probably get the flux and errors for the first and last pixel
    of the rebinned spectrum wrong.

    General pointers about rebinning if you care about errors in the
    rebinned values:

    1. Don't rebin to a smaller bin size.
    2. Be aware when you rebin you introduce correlations between
       neighbouring points and between their errors.
    3. Rebin as few times as possible.

    """
    # Note: 0 suffix indicates the old spectrum, 1 the rebinned spectrum.
    colors= 'brgy'
    debug = kwargs.pop('debug', False)
    
    # Create rebinned spectrum wavelength scale
    sp1 = Spectrum(**kwargs)
    # find pixel edges, used when rebinning
    edges0 = find_wa_edges(wav)
    edges1 = find_wa_edges(sp1.wa)
    if debug:
        pl.clf()
        x0,x1 = edges1[0:2]
        yh, = pl.bar(x0, 0, width=(x1-x0),color='gray',
                    linestyle='dotted',alpha=0.3)
    widths0 = edges0[1:] - edges0[:-1]
    npts0 = len(wav)
    npts1 = len(sp1.wa)
    df = 0.
    de2 = 0.
    npix = 0    # number of old pixels contributing to rebinned pixel,
    j = 0                # index of rebinned array
    i = 0                # index of old array

    # sanity check
    if edges0[-1] < edges1[0] or edges1[-1] < edges0[0]:
        raise ValueError('Wavelength scales do not overlap!')
    
    # find the first contributing old pixel to the rebinned spectrum
    if edges0[i+1] < edges1[0]:
        # Old wa scale extends lower than the rebinned scale. Find the
        # first old pixel that overlaps with rebinned scale.
        while edges0[i+1] < edges1[0]:
            i += 1
        i -= 1
    elif edges0[0] > edges1[j+1]:
        # New rebinned wa scale extends lower than the old scale. Find
        # the first rebinned pixel that overlaps with the old spectrum
        while edges0[0] > edges1[j+1]:
            sp1.fl[j] = np.nan
            sp1.er[j] = np.nan
            j += 1
        j -= 1
    lo0 = edges0[i]      # low edge of contr. (sub-)pixel in old scale
    while True:
        hi0 = edges0[i+1]  # upper edge of contr. (sub-)pixel in old scale
        hi1 = edges1[j+1]  # upper edge of jth pixel in rebinned scale

        if hi0 < hi1:
            if er[i] > 0:
                dpix = (hi0 - lo0) / widths0[i]
                df += fl[i] * dpix
                # We don't square dpix below, since this causes an
                # artificial variation in the rebinned errors depending on
                # how the old wav bins are divided up into the rebinned
                # wav bins.
                #
                # i.e. 0.25**2 + 0.75**2 != 0.5**2 + 0.5**2 != 1**2
                de2 += er[i]**2 * dpix
                npix += dpix
            if debug:
                yh.set_height(df/npix)
                c0 = colors[i % len(colors)]
                pl.bar(lo0, fl[i], width=hi0-lo0, color=c0, alpha=0.3)
                pl.text(lo0, fl[i], 'lo0')
                pl.text(hi0, fl[i], 'hi0')
                pl.text(hi1, fl[i], 'hi1')
                raw_input('enter...')
            lo0 = hi0
            i += 1
            if i == npts0:  break
        else:
            # We have all old pixel flux values that contribute to the
            # new pixel; append the new flux value and move to the
            # next new pixel.
            if er[i] > 0:
                dpix = (hi1 - lo0) / widths0[i]
                df += fl[i] * dpix
                de2 += er[i]**2 * dpix
                npix += dpix
            if debug:
                yh.set_height(df/npix)
                c0 = colors[i % len(colors)]
                pl.bar(lo0,  fl[i], width=hi1-lo0, color=c0, alpha=0.3)
                pl.text(lo0, fl[i], 'lo0')
                pl.text(hi0, fl[i], 'hi0')
                pl.text(hi1, fl[i], 'hi1')
                raw_input('df, de2, npix: %s %s %s   enter...' %
                          (df, de2, npix))
            if npix > 0:
                # find total flux and error, then divide by number of
                # pixels (i.e. conserve flux density).
                sp1.fl[j] = df / npix
                sp1.er[j] = sqrt(de2) / npix
            else:
                sp1.fl[j] = np.nan
                sp1.er[j] = np.nan
            df = 0.
            de2 = 0.
            npix = 0.
            lo0 = hi1
            j += 1
            if j == npts1:  break
            if debug:
                x0,x1 = edges1[j:j+2]
                yh, = pl.bar(x0, 0, width=x1-x0, color='gray',
                       linestyle='dotted', alpha=0.3)
                raw_input('enter...')

    return sp1

def combine(spectra, cliphi=None, cliplo=None, verbose=False):
    """ Combine spectra pixel by pixel, weighting by the inverse variance
    of each pixel.  Clip high sigma values by sigma times clip values
    Returns the combined spectrum.

    If the wavelength scales of the input spectra differ, combine()
    will rebin the spectra to a common linear (not log-linear)
    wavelength scale, with pixel width equal to the largest pixel
    width in the input spectra. If this is not what you want, rebin
    the spectra by hand with rebin() before using combine().
    """
    def clip(cliphi, cliplo, s_rebinned):
        # clip the rebinned input spectra

        # find pixels where we can clip: where we have at least three
        # good contributing values.
        goodpix = np.zeros(len(s_rebinned[0].wa))
        for s in s_rebinned:
            goodpix += (s.er > 0).astype(int)
        canclip = goodpix > 2
        # find median values
        medfl = np.median([s.fl[canclip] for s in s_rebinned], axis=0)
        nclipped = 0
        for i,s in enumerate(s_rebinned):
            fl = s.fl[canclip]
            er = s.er[canclip]
            diff = (fl - medfl) / er
            if cliphi is not None:
                badpix = diff > cliphi
                s_rebinned[i].er[canclip][badpix] = np.nan
                nclipped += len(badpix.nonzero()[0])
            if cliplo is not None:
                badpix = diff < -cliplo
                s_rebinned[i].er[canclip][badpix] = np.nan
                nclipped += len(badpix.nonzero()[0])
        if debug: print(nclipped, 'pixels clipped across all input spectra')
        return nclipped

    nspectra = len(spectra)
    if verbose:
        print('%s spectra to combine' % nspectra)
    if nspectra < 2:
        raise Exception('Need at least 2 spectra to combine.')

    if cliphi is not None and nspectra < 3:  cliphi = None
    if cliplo is not None and nspectra < 3:  cliplo = None

    # Check if wavescales are the same:
    spec0 = spectra[0]
    wa = spec0.wa
    npts = len(wa)
    needrebin = True
    for sp in spectra:
        if len(sp.wa) != npts:
            if verbose: print('Rebin required')
            break
        if (np.abs(sp.wa - wa) / wa[0]).max() > 1e-8:
            if verbose:
                print((np.abs(sp.wa - wa) / wa[0]).max(), 'Rebin required')
            break
    else:
        needrebin = False
        if verbose:  print('No rebin required')

    # interpolate over 1 sigma error arrays
    
    if needrebin:
        # Make wavelength scale for combined spectrum.  Only linear for now.
        wstart = min(sp.wa[0] for sp in spectra)
        wend = max(sp.wa[-1] for sp in spectra)
        # Choose largest wavelength bin size of old spectra.
        if verbose:  print('finding new bin size')
        maxwidth = max((sp.wa[1:] - sp.wa[:-1]).max() for sp in spectra)
        npts = int(np.ceil((wend - wstart) / maxwidth))      # round up
        # rebin spectra to combined wavelength scale
        if verbose:  print('Rebinning spectra')
        s_rebinned = [s.rebin(wstart=wstart, npts=npts, dw=maxwidth)
                      for s in spectra]
        combined = Spectrum(wstart=wstart, npts=npts, dw=maxwidth)
        if verbose:
            print(('New wavelength scale wstart=%s, wend=%s, npts=%s, dw=%s'
                   % (wstart, combined.wa[-1], npts, maxwidth)))
    else:
        combined = Spectrum(wa=spec0.wa)
        s_rebinned = copy.deepcopy(spectra)

    # sigma clipping, if requested
    if cliphi is not None or cliplo is not None:
        clip(cliphi, cliplo, s_rebinned)
        # repeat, clipping to 4 sigma this time
        #npixclipped = clip(4.,4.,s_rebinned)

    # Now add the spectra
    for i in range(len(combined.wa)):
        wtot = fltot = ertot = 0.
        npix = 0            # num of old spectrum pixels contributing to new
        for s in s_rebinned:
            # if not a sensible flux value, skip to the next pixel
            if s.er[i] > 0:
                npix += 1
                # Weighted mean (weight by inverse variance)
                variance = s.er[i] ** 2
                w = 1. / variance
                fltot += s.fl[i] * w
                ertot += (s.er[i] * w)**2
                wtot += w
        if npix > 0:
            combined.fl[i] = fltot / wtot
            combined.er[i] = np.sqrt(ertot) / wtot
        else:
            combined.fl[i] = np.nan
            combined.er[i] = np.nan

        #contributing.fl[i] = npix_contrib
    return combined
