#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *


# +
# +
# __doc__ string
# _
__doc__ = """test of OcsGenericEntity"""


# +
# function: test_instantiate()
# -
def test_instantiate():
    cam = None
    try:
        cam = OcsGenericEntity('CCS', 'Camera')
    except OcsGenericEntityException as a:
        print(a.errstr)
    if cam:
        assert True
    else:
        assert False


# +
# function: test_noinstantiate()
# -
def test_noinstantiate():
    junk = None
    try:
        junk = OcsGenericEntity('JUNK', 'junk')
    except OcsGenericEntityException as b:
        print(b.errstr)
    if junk:
        assert False
    else:
        assert True


# +
# function: test_nosystem()
# -
def test_nosystem():
    cam = OcsGenericEntity('CCS', 'Camera')
    if not cam:
        assert False
    else:
        try:
            cam.system = 'TCS'
        except OcsGenericEntityException:
            assert True


# +
# function: test_noentity()
# -
def test_noentity():
    cam = OcsGenericEntity('CCS', 'camera')
    if not cam:
        assert False
    else:
        try:
            cam.entity = 'telescope'
        except OcsGenericEntityException:
            assert True
