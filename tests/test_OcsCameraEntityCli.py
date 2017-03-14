#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsCameraEntityCli import *


# +
# +
# __doc__ string
# _
__doc__ = """test of OcsCameraEntityCli"""


# function: test_cli()
# -
def test_cli():
    cli = None
    try:
        cli = OcsCameraCli()
    except OcsGenericEntityException as x:
        print(x.errstr)
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
    except OcsCameraEntityException as c:
        print(c.errstr)
    except OcsGenericEntityException as x:
        print(x.errstr)
    if cli:
        assert True
    else:
        assert False
