#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *


# +
# +
# __doc__ string
# _
__doc__ = """test of OcsGenericEntityCli"""


# +
# function: test_cli()
# -
def test_cli():
    cli = None
    try:
        cli = OcsGenericEntityCli()
    except OcsGenericEntityException:
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
        cli = OcsGenericEntityCli()
        cli.execute()
    except OcsGenericEntityException as f:
        print(f.errstr)
    if cli:
        assert True
    else:
        assert False
