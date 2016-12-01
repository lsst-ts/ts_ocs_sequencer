#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsCameraEntity import *


# +
# function: test_instantiate()
# -
def test_instantiate():
    camera = None
    try:
        camera = OcsCameraEntity('CCS', 'camera')
    except OcsGenericEntityException as a:
        print(a.errstr)
        assert False
    except OcsCameraEntityException as b:
        print(b.errstr)
        assert False
    if camera:
        assert True


# +
# function: test_nosystem()
# -
def test_nosystem():
    camera = OcsCameraEntity('CCS', 'camera')
    if camera:
        try:
            camera.system = 'TCS'
        except OcsGenericEntityException as e:
            print(e.errstr)
            assert True
        except OcsCameraEntityException as f:
            print(f.errstr)
            assert True
        else:
            assert False


# +
# function: test_noentity()
# -
def test_noentity():
    camera = OcsCameraEntity('CCS', 'camera')
    if camera:
        try:
            camera.entity = 'telescope'
        except OcsGenericEntityException as g:
            print(g.errstr)
            assert True
        except OcsCameraEntityException as h:
            print(h.errstr)
            assert True
        else:
            assert False
