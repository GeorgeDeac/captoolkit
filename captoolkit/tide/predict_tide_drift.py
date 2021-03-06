#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
predict_tide_drift.py (11/2019)
Predict tidal elevation at multiple times and locations using harmonic constants

Example:
    ht = predict_tide_drift(time,hc,con)

Input:
    time: days relative to Jan 1, 1992 (48622mjd)
    hc: harmonic constant vector (complex)
    constituents: tidal constituent IDs

OUTPUT:
    ht: time series reconstructed using the nodal corrections

Options:
    DELTAT: time correction for converting to Ephemeris Time (days)
    CORRECTIONS: use nodal corrections from OTIS/ATLAS or GOT models

Requires::
    numpy: Scientific Computing Tools For Python
        http://www.numpy.org
        http://www.scipy.org/NumPy_for_Matlab_Users

Dependencies:
    load_constituent.py: loads parameters for a given tidal constituent
    load_nodal_corrections.py: loads nodal corrections for tidal constituents

History:
    Updated 11/2019: output as numpy masked arrays instead of nan-filled arrays
    Updated 09/2019: added netcdf option to CORRECTIONS option
    Updated 08/2018: added correction option ATLAS for localized OTIS solutions
    Updated 07/2018: added option to use GSFC GOT nodal corrections
    Updated 09/2017: Rewritten in Python
"""
import numpy as np
from load_constituent import load_constituent
from load_nodal_corrections import load_nodal_corrections

def predict_tide_drift(time,hc,constituents,DELTAT=0.0,CORRECTIONS='OTIS'):
    nt = len(time)
    # load the nodal corrections
    pu,pf,G = load_nodal_corrections(time + 48622.0, constituents,
        DELTAT=DELTAT, CORRECTIONS=CORRECTIONS)
    # allocate for output time series
    ht = np.ma.zeros((nt))
    # for each constituent
    for k,c in enumerate(constituents):
        if CORRECTIONS in ('OTIS','ATLAS','netcdf'):
            # load parameters for each constituent
            amp,ph,omega,alpha,species = load_constituent(c)
            # add component for constituent to output tidal elevation
            th = omega*time*86400.0 + ph + pu[:,k]
        elif (CORRECTIONS == 'GOT'):
            th = G[:,k]*np.pi/180.0 + pu[:,k]
        # sum over all tides
        ht += pf[:,k]*hc.real[:,k]*np.cos(th) - pf[:,k]*hc.imag[:,k]*np.sin(th)
    # return the tidal elevation
    return ht
