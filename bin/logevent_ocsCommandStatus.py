#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import time
from OcsLogger import *
from SALPY_ocs import *


# +
# __doc__ string
# -
__doc__ = """Event logger for specific event in the OCS"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "logevent_ocsCommandStatus.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# main()
# -
if __name__ == "__main__":

    # get a logger
    evlog = OcsLogger('Events', 'ocsCommandStatus')
    evlog.logger.info('{0:s} starting up'.format(__file__))

    # connect to SAL
    mgr = SAL_ocs()

    # set up for specific event
    mgr.salEvent('ocs_logevent_ocsCommandStatus')

    # create event container
    event = ocs_logevent_ocsCommandStatusC()

    # log message
    evlog.logger.info('{0:s} ready'.format(__file__))

    # loop forever
    while True:
        retval = mgr.getEvent_ocsCommandStatus(event)
        if retval == 0:
            evlog.logger.info('{0:s} event received'.format(__file__))
            evlog.logger.info('\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
            evlog.logger.info('\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
            evlog.logger.info('\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
            evlog.logger.info('\tevent.priority       = {0:d}'.format(event.priority))
            evlog.logger.info('\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
            evlog.logger.info('\tevent.Status         = {0:s}'.format(event.Status))
            evlog.logger.info('\tevent.StatusValue    = {0:d}'.format(event.StatusValue))
            evlog.logger.info('\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
        time.sleep(1)

    # enable this code if we can terminate the infinite loop above
    # evlog.logger.info('{0:s} shutting down'.format(__file__))
    # mgr.salShutdown()
    # exit()
