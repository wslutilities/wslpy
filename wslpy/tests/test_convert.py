# -*- coding: utf-8 -*-
__author__ = 'Patrick Wu'
from nose.tools import assert_equal, raises

import  unittest
import wslpy.convert as wconvert


def setUp():
    pass


def teardown():
    pass


def test_to_win():
    result=wconvert.to("C:\\test")
    assert_equal("/mnt/C/test", result)


def test_to_windouble():
    result=wconvert.to("C:\\\\test")
    assert_equal("/mnt/C/test", result)


def test_to_linux():
    result=wconvert.to("/mnt/c/test")
    assert_equal("c:\\test", result)


@raises(ValueError)
def test_to_invalid():
    wconvert.to("/mnt/c/test", 'NoneSense')


def test_towin_win():
    result=wconvert.to_win("C:\\test")
    assert_equal("C:\\test", result)


def test_towin_windouble():
    result=wconvert.to_win("C:\\\\test")
    assert_equal("C:\\test", result)


def test_towin_linux():
    result=wconvert.to_win("/mnt/c/test")
    assert_equal("c:\\test", result)


def test_towindouble_win():
    result=wconvert.to_win_double("C:\\test")
    assert_equal("C:\\\\test", result)


def test_towindouble_windouble():
    result=wconvert.to_win_double("C:\\\\test")
    assert_equal("C:\\\\test", result)


def test_towindouble_linux():
    result=wconvert.to_win_double("/mnt/c/test")
    assert_equal("c:\\\\test", result)


def test_towsl_win():
    result=wconvert.to_wsl("C:\\test")
    assert_equal("/mnt/C/test", result)


def test_towsl_windouble():
    result=wconvert.to_wsl("C:\\\\test")
    assert_equal("/mnt/C/test", result)


def test_towsl_linux():
    result=wconvert.to_wsl("/mnt/c/test")
    assert_equal("/mnt/c/test", result)