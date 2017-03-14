#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsCameraEntity import *


# +
# __doc__ string
# _
__doc__ = """test of OcsCameraEntity"""


# +
# function: test_instantiate()
# -
def test_instantiate():
    try:
        cam = OcsCameraEntity('CCS', 'camera')
    except OcsGenericEntityException as a:
        print(a.errstr)
        assert False
    if cam:
        assert True


# +
# function: test_nosystem()
# -
def test_nosystem():
    cam = OcsCameraEntity('CCS', 'camera')
    if cam:
        try:
            cam.system = 'TCS'
        except OcsCameraEntityException as c:
            print(c.errstr)
        except OcsGenericEntityException as g:
            print(g.errstr)
            assert True
        else:
            assert False


# +
# function: test_noentity()
# -
def test_noentity():
    cam = OcsCameraEntity('CCS', 'camera')
    if cam:
        try:
            cam.entity = 'telescope'
        except OcsCameraEntityException as c:
            print(c.errstr)
        except OcsGenericEntityException as g:
            print(g.errstr)
            assert True
        else:
            assert False
