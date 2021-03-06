# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division
import itertools


import numpy as np
from numpy.testing import assert_array_equal
from nose.tools import eq_ as eq


from numcodecs.fixedscaleoffset import FixedScaleOffset
from numcodecs.tests.common import check_encode_decode, check_config, \
    check_repr


arrs = [
    np.linspace(1000, 1001, 1000, dtype='f8'),
    np.random.normal(loc=1000, scale=1, size=1000).astype('f8'),
    np.linspace(1000, 1001, 1000, dtype='f8').reshape(100, 10),
    np.linspace(1000, 1001, 1000, dtype='f8').reshape(100, 10, order='F'),
    np.linspace(1000, 1001, 1000, dtype='f8').reshape(10, 10, 10),
]


codecs = [
    FixedScaleOffset(offset=1000, scale=10, dtype='f8', astype='i1'),
    FixedScaleOffset(offset=1000, scale=10**2, dtype='f8', astype='i2'),
    FixedScaleOffset(offset=1000, scale=10**6, dtype='f8', astype='i4'),
    FixedScaleOffset(offset=1000, scale=10**12, dtype='f8', astype='i8'),
    FixedScaleOffset(offset=1000, scale=10**12, dtype='f8'),
]


def test_encode_decode():
    for arr, codec in itertools.product(arrs, codecs):
        precision = int(np.log10(codec.scale))
        check_encode_decode(arr, codec, precision=precision)


def test_encode():
    dtype = '<f8'
    astype = '|u1'
    codec = FixedScaleOffset(scale=10, offset=1000, dtype=dtype,
                             astype=astype)
    arr = np.linspace(1000, 1001, 10, dtype=dtype)
    expect = np.array([0, 1, 2, 3, 4, 6, 7, 8, 9, 10], dtype=astype)
    actual = codec.encode(arr)
    assert_array_equal(expect, actual)
    eq(np.dtype(astype), actual.dtype)


def test_config():
    codec = FixedScaleOffset(dtype='<f8', astype='<i4', scale=10, offset=100)
    check_config(codec)


def test_repr():
    stmt = "FixedScaleOffset(scale=10, offset=100, dtype='<f8', astype='<i4')"
    check_repr(stmt)
