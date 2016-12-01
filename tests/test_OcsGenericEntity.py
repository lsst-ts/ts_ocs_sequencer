#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsGenericEntity import *


# +
# function: test_instantiate()
# -
def test_instantiate():
    camera = None
    try:
        camera = OcsGenericEntity('CCS', 'camera')
    except OcsGenericEntityException as a:
        print(a.errstr)
        assert False
    if camera is not None:
        assert True


# +
# function: test_noinstantiate()
# -
def test_noinstantiate():
    junk = None
    try:
        junk = OcsGenericEntity('JUNK', 'junk')
    except OcsGenericEntityException as b:
        print(b.errstr)
        assert True
    if junk is not None:
        assert False


# +
# function: test_nosystem()
# -
def test_nosystem():
    camera = OcsGenericEntity('CCS', 'camera')
    if camera is not None:
        try:
            camera.system = 'TCS'
        except OcsGenericEntityException as c:
            print(c.errstr)
        if c:
            assert True
        else:
            assert False


# +
# function: test_noentity()
# -
def test_noentity():
    camera = OcsGenericEntity('CCS', 'camera')
    if camera is not None:
        try:
            camera.entity = 'telescope'
        except OcsGenericEntityException as c:
            print(c.errstr)
        if c:
            assert True
        else:
            assert False

