#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
import sys
import time
from ocs_common import *
from OcsLogger import *
from SALPY_ocs import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Event logger for specific event in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "logevent_ocsCommandIssued.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# main()
# -
if __name__ == "__main__":

    # get a logger
    evlog = OcsLogger('Events', 'ocsCommandIssued')
    evlog.logger.info('{0:s} starting up'.format(sys.argv[0]))

    # connect to SAL
    mgr = SAL_ocs()

    # set up for specific event
    mgr.salEvent('ocs_logevent_ocsCommandIssued')

    # create event container
    event = ocs_logevent_ocsCommandIssuedC()

    # log message
    evlog.logger.info('{0:s} ready'.format(sys.argv[0]))

    # loop forever
    while True:
        retval = mgr.getEvent_ocsCommandIssued(event)
        if retval == 0:
            evlog.logger.info('{0:s} event received'.format(sys.argv[0]))
            evlog.logger.info('\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
            evlog.logger.info('\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
            evlog.logger.info('\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
            evlog.logger.info('\tevent.priority       = {0:d}'.format(event.priority))
            evlog.logger.info('\tevent.ReturnValue    = {0:d}'.format(event.ReturnValue))
            evlog.logger.info('\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
            evlog.logger.info('\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
        time.sleep(1)

    # shutdown
    evlog.logger.info('{0:s} shutting down'.format(sys.argv[0]))
    mgr.salShutdown()
    exit()
