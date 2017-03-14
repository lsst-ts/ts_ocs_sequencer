#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import time
from OcsLogger import *
from SALPY_archiver import *


# +
# __doc__ string
# -
__doc__ = """Event logger for specific event in the DMCS Archiver"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "logevent_archiverEntitySummaryState.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# main()
# -
if __name__ == "__main__":

    # get a logger
    evlog = OcsLogger('Events', 'archiverEntitySummaryState')
    evlog.logger.info('{0:s} starting up'.format(__file__))

    # connect to SAL
    mgr = SAL_archiver()

    # set up for specific event
    mgr.salEvent('archiver_logevent_archiverEntitySummaryState')

    # create event container
    event = archiver_logevent_archiverEntitySummaryStateC()

    # log message
    evlog.logger.info('{0:s} ready'.format(__file__))

    # loop forever
    while True:
        retval = mgr.getEvent_archiverEntitySummaryState(event)
        if retval == 0:
            evlog.logger.info('{0:s} event received'.format(__file__))
            evlog.logger.info('\tevent.Address                 = {0:d}'.format(event.Address))
            evlog.logger.info('\tevent.CommandsAvailable       = {0:s}'.format(event.CommandsAvailable))
            evlog.logger.info('\tevent.ConfigurationsAvailable = {0:s}'.format(event.ConfigurationsAvailable))
            evlog.logger.info('\tevent.Executing               = {0:s}'.format(event.Executing))
            evlog.logger.info('\tevent.Identifier              = {0:.17f}'.format(event.Identifier))
            evlog.logger.info('\tevent.Name                    = {0:s}'.format(event.Name))
            evlog.logger.info('\tevent.CurrentState            = {0:s}'.format(event.CurrentState))
            evlog.logger.info('\tevent.PreviousState           = {0:s}'.format(event.PreviousState))
            evlog.logger.info('\tevent.Timestamp               = {0:s}'.format(event.Timestamp))
            evlog.logger.info('\tevent.priority                = {0:d}'.format(event.priority))
        time.sleep(1)

    # shutdown
    # evlog.logger.info('{0:s} shutting down'.format(__file__))
    # mgr.salShutdown()
    # exit()
