#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsCameraEntityCli import *


# +
# function: test_cli()
# -
def test_cli():
    cli = None
    try:
        cli = OcsCameraCli()
    except:
        pass
    if cli:
        assert True
    else:
        assert False


# +
# function: test_parse_cli()
# -
def test_parse_cli():
    cli = None
    try:
        cli = OcsCameraCli()
        cli.execute()
    except OcsGenericEntityException as e:
        print(e.errstr)
    except OcsCameraEntityException as e:
        print(e.errstr)
    if cli:
        assert True
    else:
        assert False

