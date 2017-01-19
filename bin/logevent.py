#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import sys
import threading
import time
from ocs_common import *
from ocs_sal import *
from OcsLogger import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__doc__ = """Event logger for any events"""
__email__ = "pdaly@lsst.org"
__file__ = "logevent.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: camera_payload()
# -
def camera_payload(log=None, event='', payload=None):
    if log and (isinstance(event,str) and event!='') and payload:
        pass

# function: ocs_payload()
# -
# +
def ocs_payload(log=None, event='', payload=None):
    if log and (isinstance(event,str) and event!='') and payload:
        if event == 'ocsCommandIssued':
            log.logger.info('\tpayload.CommandSent    = {0:s}'.format(payload.CommandSent))
            log.logger.info('\tpayload.CommandSource  = {0:s}'.format(payload.CommandSource))
            log.logger.info('\tpayload.Identifier     = {0:.17f}'.format(payload.Identifier))
            log.logger.info('\tpayload.priority       = {0:d}'.format(payload.priority))
            log.logger.info('\tpayload.ReturnValue    = {0:d}'.format(payload.ReturnValue))
            log.logger.info('\tpayload.SequenceNumber = {0:d}'.format(payload.SequenceNumber))
            log.logger.info('\tpayload.Timestamp      = {0:s}'.format(payload.Timestamp))
        elif event == 'ocsCommandStatus':
            log.logger.info('\tpayload.CommandSource  = {0:s}'.format(payload.CommandSource))
            log.logger.info('\tpayload.CommandSent    = {0:s}'.format(payload.CommandSent))
            log.logger.info('\tpayload.Identifier     = {0:.17f}'.format(payload.Identifier))
            log.logger.info('\tpayload.priority       = {0:d}'.format(payload.priority))
            log.logger.info('\tpayload.SequenceNumber = {0:d}'.format(payload.SequenceNumber))
            log.logger.info('\tpayload.Status         = {0:s}'.format(payload.Status))
            log.logger.info('\tpayload.StatusValue    = {0:d}'.format(payload.StatusValue))
            log.logger.info('\tpayload.Timestamp      = {0:s}'.format(payload.Timestamp))
        elif event == 'ocsEntityShutdown':
            log.logger.info('\tpayload.Name       = {0:s}'.format(payload.Name))
            log.logger.info('\tpayload.Identifier = {0:.17f}'.format(payload.Identifier))
            log.logger.info('\tpayload.Timestamp  = {0:s}'.format(payload.Timestamp))
            log.logger.info('\tpayload.Address    = {0:d}'.format(payload.Address))
            log.logger.info('\tpayload.priority   = {0:d}'.format(payload.priority))
        elif event == 'ocsEntityStartup':
            log.logger.info('\tpayload.Name       = {0:s}'.format(payload.Name))
            log.logger.info('\tpayload.Identifier = {0:.17f}'.format(payload.Identifier))
            log.logger.info('\tpayload.Timestamp  = {0:s}'.format(payload.Timestamp))
            log.logger.info('\tpayload.Address    = {0:d}'.format(payload.Address))
            log.logger.info('\tpayload.priority   = {0:d}'.format(payload.priority))


# function: thread_code()
# -
def thread_code(entity='', event=''):

    # check input(s)
    if not isinstance(entity,str) or entity=='':
        return
    if not isinstance(event,str) or event=='':
        return

    # get logger
    evlog = OcsLogger('Events', event)
    evlog.logger.info('{0:s} thread starting up'.format(event))


    # import SAL
    sal = ocs_sal_import('SALPY_{0:s}'.format(entity))
    if not sal:
        return
    evlog.logger.info('{0:s} thread connected to SAL'.format(event))

    # set up for event
    mgf = ocs_sal_attribute(sal, 'SAL_{0:s}'.format(entity))
    mgr = mgf()
    mgr.salEvent('{0:s}_logevent_{1:s}'.format(entity, event))
    evlog.logger.info('{0:s} thread ready'.format(event))

    # get container
    evp = ocs_sal_attribute(sal, '{0:s}_logevent_{1:s}C'.format(entity, event))
    if not evp:
        return
    payload = evp()
    evlog.logger.info('{0:s} thread container created'.format(event))

    # get event function
    evf = ocs_sal_attribute(mgr, 'getEvent_{0:s}'.format(event))
    if not evf:
        return
    evlog.logger.info('{0:s} thread container created'.format(event))

    # loop forever
    while True:
        retval = evf(payload)
        if retval == 0:
            evlog.logger.info('{0:s} thread event received'.format(event))
            if hasattr(sys.modules[__name__], '{0:s}_payload'.format(entity)):
                pf = getattr(sys.modules[__name__], '{0:s}_payload'.format(entity))
                pf(evlog, event, payload)
            else:
                pass
        time.sleep(1)

    evlog.logger.info('thread {0:s} shutting down'.format(event))
    return True

# +
# main()
# -
if __name__ == "__main__":

    # list of events
    ccs_events = [ 'ccsConfigured', 'endInitializeGuider', 'endInitializeImage', 'endLoadFilter',
        'endReadout', 'endRotateCarousel', 'endSetFilter', 'endShutterClose', 'endShutterOpen',
        'endTakeImage', 'endUnloadFilter', 'notReadyToTakeImage', 'prepareToTakeImage', 'readyToTakeImage',
        'startIntegration', 'startLoadFilter', 'startReadout', 'startRotateCarousel', 'startSetFilter',
        'startShutterClose', 'startShutterOpen', 'startUnloadFilter' ]

    ocs_events = [ 'ocsCommandIssued', 'ocsCommandStatus', 'ocsEntityShutdown', 'ocsEntityStartup' ]

    # create threads for ccs_events:
    ccs_threads = []
    for T in ccs_events:
        c = threading.Thread(name=T, target=thread_code, args=('camera', T,))
        ccs_threads.append(c)
        c.start()

    # create threads for ocs_events:
    ocs_threads = []
    for T in ocs_events:
        o = threading.Thread(name=T, target=thread_code, args=('ocs', T,))
        ocs_threads.append(o)
        o.start()
