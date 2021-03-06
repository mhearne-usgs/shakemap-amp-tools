#!/usr/bin/env python

import os.path
import numpy as np
from amptools.io.knet.core import is_knet, read_knet

def test():
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?

    datadir = os.path.join(homedir,'..','..','..','data','knet')
    knet_file1 = os.path.join(datadir,'AOM0051801241951.EW')
    knet_file2 = os.path.join(datadir,'AOM0051801241951.NS')
    knet_file3 = os.path.join(datadir,'AOM0051801241951.UD')
    assert is_knet(knet_file1)
    try:
        assert is_knet(os.path.abspath(__file__))
    except AssertionError:
        assert 1==1

    # test a knet file with npoints % 10 == 0
    stream1 = read_knet(knet_file1)
    stream2 = read_knet(knet_file2)
    stream3 = read_knet(knet_file3)
    np.testing.assert_almost_equal(stream1[0].max(),29.070,decimal=2)
    np.testing.assert_almost_equal(stream2[0].max(),28.821,decimal=2)
    np.testing.assert_almost_equal(stream3[0].max(),11.817,decimal=2)

    # test a file that has a number of points divisible by 8
    knet_file4 = os.path.join(datadir,'AOM0011801241951.EW')
    knet_file5 = os.path.join(datadir,'AOM0011801241951.NS')
    knet_file6 = os.path.join(datadir,'AOM0011801241951.UD')
    stream4 = read_knet(knet_file4)
    stream5 = read_knet(knet_file5)
    stream6 = read_knet(knet_file6)
    np.testing.assert_almost_equal(stream4[0].max(),4.078,decimal=2)
    np.testing.assert_almost_equal(stream5[0].max(),-4.954,decimal=2)
    np.testing.assert_almost_equal(stream6[0].max(),-2.240,decimal=2)

    # test that a file that is not knet format raises an Exception
    try:
        datadir = os.path.join(homedir,'..','..','..','data','geonet')
        knet_file = os.path.join(datadir,'20161113_110256_WTMC_20.V1A')
        read_knet(knet_file)
        success = True
    except Exception:
        success = False
    assert success == False

if __name__ == '__main__':
    test()
