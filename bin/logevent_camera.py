#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import sys
import threading
import time
from ocs_common import *
from OcsLogger import *
from SALPY_camera import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__doc__ = """Event logger for all events in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "logevent_camera.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: thread_code()
# -
def thread_code():

    # get thread name
    thread_name = threading.currentThread().getName();

    # get logger
    evlog = OcsLogger('Events', thread_name)
    evlog.logger.info('{0:s} thread starting up'.format(thread_name))

    # connect to SAL
    mgr = SAL_camera()
    if not mgr:
        return
    evlog.logger.info('{0:s} thread connected to SAL'.format(thread_name))

    # set up for event
    mgr.salEvent('camera_logevent_{0:s}'.format(thread_name))
    evlog.logger.info('{0:s} thread ready'.format(thread_name))

    # get container
    if thread_name == 'ccsConfigured':
        event = camera_logevent_ccsConfiguredC()
    elif thread_name == 'endInitializeGuider':
        event = camera_logevent_endInitializeGuiderC()
    elif thread_name == 'endInitializeImage':
        event = camera_logevent_endInitializeImageC()
    elif thread_name == 'endLoadFilter':
        event = camera_logevent_endLoadFilterC()
    elif thread_name == 'endReadout':
         event = camera_logevent_endReadoutC()
    elif thread_name == 'endRotateCarousel':
        event = camera_logevent_endRotateCarouselC()
    elif thread_name == 'endSetFilter':
        event = camera_logevent_endSetFilterC()
    elif thread_name == 'endShutterClose':
        event = camera_logevent_endShutterCloseC()
    elif thread_name == 'endShutterOpen':
        event = camera_logevent_endShutterOpenC()
    elif thread_name == 'endTakeImage':
        event = camera_logevent_endTakeImageC()
    elif thread_name == 'endUnloadFilter':
        event = camera_logevent_endUnloadFilterC()
    elif thread_name == 'notReadyToTakeImage':
        event = camera_logevent_notReadyToTakeImageC()
    elif thread_name == 'prepareToTakeImage':
        event = camera_logevent_prepareToTakeImageC()
    elif thread_name == 'readyToTakeImage':
        event = camera_logevent_readyToTakeImageC()
    elif thread_name == 'startIntegration':
        event = camera_logevent_startIntegrationC()
    elif thread_name == 'startLoadFilter':
        event = camera_logevent_startLoadFilterC()
    elif thread_name == 'startReadout':
        event = camera_logevent_startReadoutC()
    elif thread_name == 'startRotateCarousel':
        event = camera_logevent_startRotateCarouselC()
    elif thread_name == 'startSetFilter':
        event = camera_logevent_startSetFilterC()
    elif thread_name == 'startShutterClose':
        event = camera_logevent_startShutterCloseC()
    elif thread_name == 'startShutterOpen':
        event = camera_logevent_startShutterOpenC()
    elif thread_name == 'startUnloadFilter':
        event = camera_logevent_startUnloadFilterC()
    else:
        return False
    evlog.logger.info('{0:s} thread container created'.format(thread_name))

    # loop forever
    while True:
        if thread_name == 'ccsConfigured':
            retval = mgr.getEvent_ccsConfigured(event)
        elif thread_name == 'endInitializeGuider':
            retval = mgr.getEvent_endInitializeGuider(event)
        elif thread_name == 'endInitializeImage':
            retval = mgr.getEvent_endInitializeImage(event)
        elif thread_name == 'endLoadFilter':
            retval = mgr.getEvent_endLoadFilter(event)
        elif thread_name == 'endReadout':
            retval = mgr.getEvent_endReadout(event)
        elif thread_name == 'endRotateCarousel':
            retval = mgr.getEvent_endRotateCarousel(event)
        elif thread_name == 'endSetFilter':
            retval = mgr.getEvent_endSetFilter(event)
        elif thread_name == 'endShutterClose':
            retval = mgr.getEvent_endShutterClose(event)
        elif thread_name == 'endShutterOpen':
            retval = mgr.getEvent_endShutterOpen(event)
        elif thread_name == 'endTakeImage':
            retval = mgr.getEvent_endTakeImage(event)
        elif thread_name == 'endUnloadFilter':
            retval = mgr.getEvent_endUnloadFilter(event)
        elif thread_name == 'notReadyToTakeImage':
            retval = mgr.getEvent_notReadyToTakeImage(event)
        elif thread_name == 'prepareToTakeImage':
            retval = mgr.getEvent_prepareToTakeImage(event)
        elif thread_name == 'readyToTakeImage':
            retval = mgr.getEvent_readyToTakeImage(event)
        elif thread_name == 'startIntegration':
            retval = mgr.getEvent_startIntegration(event)
        elif thread_name == 'startLoadFilter':
            retval = mgr.getEvent_startLoadFilter(event)
        elif thread_name == 'startReadout':
            retval = mgr.getEvent_startReadout(event)
        elif thread_name == 'startRotateCarousel':
            retval = mgr.getEvent_startRotateCarousel(event)
        elif thread_name == 'startSetFilter':
            retval = mgr.getEvent_startSetFilter(event)
        elif thread_name == 'startShutterClose':
            retval = mgr.getEvent_startShutterClose(event)
        elif thread_name == 'startShutterOpen':
            retval = mgr.getEvent_startShutterOpen(event)
        elif thread_name == 'startUnloadFilter':
            retval = mgr.getEvent_startUnloadFilter(event)
        else:
            return False

        if retval == 0:
            evlog.logger.info('{0:s} thread event received'.format(thread_name))
            if thread_name == 'ccsConfigured':
                pass
            elif thread_name == 'endInitializeGuider':
                pass
            elif thread_name == 'endInitializeImage':
                pass
            elif thread_name == 'endLoadFilter':
                pass
            elif thread_name == 'endReadout':
                pass
            elif thread_name == 'endRotateCarousel':
                pass
            elif thread_name == 'endSetFilter':
                pass
            elif thread_name == 'endShutterClose':
                pass
            elif thread_name == 'endShutterOpen':
                pass
            elif thread_name == 'endTakeImage':
                pass
            elif thread_name == 'endUnloadFilter':
                pass
            elif thread_name == 'notReadyToTakeImage':
                pass
            elif thread_name == 'prepareToTakeImage':
                pass
            elif thread_name == 'readyToTakeImage':
                pass
            elif thread_name == 'startIntegration':
                evlog.logger.info('\tevent.imageName = {0:s}'.format(event.imageName))
            elif thread_name == 'startLoadFilter':
                pass
            elif thread_name == 'startReadout':
                pass
            elif thread_name == 'startRotateCarousel':
                pass
            elif thread_name == 'startSetFilter':
                pass
            elif thread_name == 'startShutterClose':
                pass
            elif thread_name == 'startShutterOpen':
                pass
            elif thread_name == 'startUnloadFilter':
                pass
            else:
                pass
        time.sleep(1)

    evlog.logger.info('thread {0:s} shutting down'.format(thread_name))
    return True

# +
# main()
# -
if __name__ == "__main__":

    # list of events
    events = [ 'ccsConfigured', 'endInitializeGuider', 'endInitializeImage', 'endLoadFilter',
        'endReadout', 'endRotateCarousel', 'endSetFilter', 'endShutterClose', 'endShutterOpen',
        'endTakeImage', 'endUnloadFilter', 'notReadyToTakeImage', 'prepareToTakeImage', 'readyToTakeImage',
        'startIntegration', 'startLoadFilter', 'startReadout', 'startRotateCarousel', 'startSetFilter',
        'startShutterClose', 'startShutterOpen', 'startUnloadFilter' ]

    # create threads for each event:
    threads = []
    for T in events:
        t = threading.Thread(name=T, target=thread_code)
        threads.append(t)
        t.start()
