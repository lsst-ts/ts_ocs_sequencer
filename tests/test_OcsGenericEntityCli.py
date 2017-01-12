#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *


# +
# function: test_cli()
# -
def test_cli():
    cli = None
    try:
        cli = OcsGenericEntityCli()
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
        cli = OcsGenericEntityCli()
        cli.execute()
    except OcsGenericEntityException as e:
        print(e.errstr)
    if cli:
        assert True
    else:
        assert False

