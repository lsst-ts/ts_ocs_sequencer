#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import threading
import time
from OcsLogger import *
from SALPY_ocs import *

# +
# __doc__ string
# -
__doc__ = """Event logger for events in the OCS"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "logevent_ocs.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: thread_code()
# -
def thread_code():

    # get thread name
    thread_name = threading.currentThread().getName()

    # get logger
    evlog = OcsLogger('Events', thread_name)
    evlog.logger.info('{0:s} thread starting up'.format(thread_name))

    # connect to SAL
    mgr = SAL_ocs()
    if not mgr:
        return
    evlog.logger.info('{0:s} thread connected to SAL'.format(thread_name))

    # set up for event
    mgr.salEvent('ocs_logevent_{0:s}'.format(thread_name))
    evlog.logger.info('{0:s} thread ready'.format(thread_name))

    # get container
    if thread_name == 'ocsCommandIssued':
        event = ocs_logevent_ocsCommandIssuedC()
    elif thread_name == 'ocsCommandStatus':
        event = ocs_logevent_ocsCommandStatusC()
    elif thread_name == 'ocsEntityShutdown':
        event = ocs_logevent_ocsEntityShutdownC()
    elif thread_name == 'ocsEntityStartup':
        event = ocs_logevent_ocsEntityStartupC()
    elif thread_name == 'ocsEntitySummaryState':
        event = ocs_logevent_ocsEntitySummaryStateC()
    else:
        return False
    evlog.logger.info('{0:s} thread container created'.format(thread_name))

    # loop forever
    while True:
        if thread_name == 'ocsCommandIssued':
            retval = mgr.getEvent_ocsCommandIssued(event)
        elif thread_name == 'ocsCommandStatus':
            retval = mgr.getEvent_ocsCommandStatus(event)
        elif thread_name == 'ocsEntityShutdown':
            retval = mgr.getEvent_ocsEntityShutdown(event)
        elif thread_name == 'ocsEntityStartup':
            retval = mgr.getEvent_ocsEntityStartup(event)
        elif thread_name == 'ocsEntitySummaryState':
            retval = mgr.getEvent_ocsEntitySummaryState(event)
        else:
            return False

        if retval == 0:
            evlog.logger.info('{0:s} thread event received'.format(thread_name))
            if thread_name == 'ocsCommandIssued':
                evlog.logger.info('\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
                evlog.logger.info('\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
                evlog.logger.info('\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
                evlog.logger.info('\tevent.priority       = {0:d}'.format(event.priority))
                evlog.logger.info('\tevent.ReturnValue    = {0:d}'.format(event.ReturnValue))
                evlog.logger.info('\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
                evlog.logger.info('\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
            elif thread_name == 'ocsCommandStatus':
                evlog.logger.info('\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
                evlog.logger.info('\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
                evlog.logger.info('\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
                evlog.logger.info('\tevent.priority       = {0:d}'.format(event.priority))
                evlog.logger.info('\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
                evlog.logger.info('\tevent.Status         = {0:s}'.format(event.Status))
                evlog.logger.info('\tevent.StatusValue    = {0:d}'.format(event.StatusValue))
                evlog.logger.info('\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
            elif thread_name == 'ocsEntityShutdown':
                evlog.logger.info('\tevent.Address    = {0:d}'.format(event.Address))
                evlog.logger.info('\tevent.Identifier = {0:.17f}'.format(event.Identifier))
                evlog.logger.info('\tevent.priority   = {0:d}'.format(event.priority))
                evlog.logger.info('\tevent.Name       = {0:s}'.format(event.Name))
                evlog.logger.info('\tevent.Timestamp  = {0:s}'.format(event.Timestamp))
            elif thread_name == 'ocsEntityStartup':
                evlog.logger.info('\tevent.Address    = {0:d}'.format(event.Address))
                evlog.logger.info('\tevent.Name       = {0:s}'.format(event.Name))
                evlog.logger.info('\tevent.priority   = {0:d}'.format(event.priority))
                evlog.logger.info('\tevent.Identifier = {0:.17f}'.format(event.Identifier))
                evlog.logger.info('\tevent.Timestamp  = {0:s}'.format(event.Timestamp))
            elif thread_name == 'ocsEntitySummaryState':
                evlog.logger.info('\tevent.Address                 = {0:d}'.format(event.Address))
                evlog.logger.info('\tevent.CommandsAvailable       = {0:s}'.format(event.CommandsAvailable))
                evlog.logger.info('\tevent.ConfigurationsAvailable = {0:s}'.format(event.ConfigurationsAvailable))
                evlog.logger.info('\tevent.Executing               = {0:s}'.format(event.Executing))
                evlog.logger.info('\tevent.Identifier              = {0:.17f}'.format(event.Identifier))
                evlog.logger.info('\tevent.Name                    = {0:s}'.format(event.Name))
                evlog.logger.info('\tevent.CurrentState            = {0:s}'.format(event.CurrentState))
                evlog.logger.info('\tevent.PreviousState           = {0:s}'.format(event.PreviousState))
                evlog.logger.info('\tevent.priority                = {0:d}'.format(event.priority))
                evlog.logger.info('\tevent.Timestamp               = {0:s}'.format(event.Timestamp))
            else:
                pass
        time.sleep(1)

    # enable this code if we can terminate the infinite loop above
    # evlog.logger.info('thread {0:s} shutting down'.format(thread_name))
    # return True


# +
# main()
# -
if __name__ == "__main__":

    # create threads for each event:
    threads = []
    for T in ['ocsCommandIssued', 'ocsCommandStatus', 'ocsEntityShutdown', 'ocsEntityStartup', 'ocsEntitySummaryState']:
        t = threading.Thread(name=T, target=thread_code)
        threads.append(t)
        t.start()
