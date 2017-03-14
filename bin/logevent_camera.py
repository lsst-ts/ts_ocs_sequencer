#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import threading
import time
from OcsLogger import *
from SALPY_camera import *


# +
# __doc__ string
# -
__doc__ = """Event logger for camera events in the OCS"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "logevent_camera.py"
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
    mgr = SAL_camera()
    if not mgr:
        return False
    evlog.logger.info('{0:s} thread connected to SAL'.format(thread_name))

    # set up for event
    mgr.salEvent('camera_logevent_{0:s}'.format(thread_name))
    evlog.logger.info('{0:s} thread ready'.format(thread_name))

    # get container
    event = get_event_container(thread_name)
    if not event:
        return False
    evlog.logger.info('{0:s} thread container created'.format(thread_name))

    # loop forever
    while True:
        retval = get_event_retval(thread_name, mgr, event)

        if retval != 0:
            return False
        else:
            evlog.logger.info('{0:s} thread event received'.format(thread_name))
            msg = event_response(event)
            if msg != '':
                evlog.logger.info(msg)

        time.sleep(1)

    # enable this code if we can evaluate the infinite loop above
    # evlog.logger.info('thread {0:s} shutting down'.format(thread_name))
    # return True


# +
# function: get_event_container()
# -
def get_event_container(name=''):
    if not isinstance(name, str) or name == '':
        return None
    if name == 'ccsConfigured':
        return camera_logevent_ccsConfiguredC()
    elif name == 'endInitializeGuider':
        return camera_logevent_endInitializeGuiderC()
    elif name == 'endInitializeImage':
        return camera_logevent_endInitializeImageC()
    elif name == 'endLoadFilter':
        return camera_logevent_endLoadFilterC()
    elif name == 'endReadout':
        return camera_logevent_endReadoutC()
    elif name == 'endRotateCarousel':
        return camera_logevent_endRotateCarouselC()
    elif name == 'endSetFilter':
        return camera_logevent_endSetFilterC()
    elif name == 'endShutterClose':
        return camera_logevent_endShutterCloseC()
    elif name == 'endShutterOpen':
        return camera_logevent_endShutterOpenC()
    elif name == 'endTakeImage':
        return camera_logevent_endTakeImageC()
    elif name == 'endUnloadFilter':
        return camera_logevent_endUnloadFilterC()
    elif name == 'notReadyToTakeImage':
        return camera_logevent_notReadyToTakeImageC()
    elif name == 'prepareToTakeImage':
        return camera_logevent_prepareToTakeImageC()
    elif name == 'readyToTakeImage':
        return camera_logevent_readyToTakeImageC()
    elif name == 'startIntegration':
        return camera_logevent_startIntegrationC()
    elif name == 'startLoadFilter':
        return camera_logevent_startLoadFilterC()
    elif name == 'startReadout':
        return camera_logevent_startReadoutC()
    elif name == 'startRotateCarousel':
        return camera_logevent_startRotateCarouselC()
    elif name == 'startSetFilter':
        return camera_logevent_startSetFilterC()
    elif name == 'startShutterClose':
        return camera_logevent_startShutterCloseC()
    elif name == 'startShutterOpen':
        return camera_logevent_startShutterOpenC()
    elif name == 'startUnloadFilter':
        return camera_logevent_startUnloadFilterC()
    else:
        return None


# +
# function: get_event_retval()
# -
def get_event_retval(name='', mgr=None, event=None):
    if not isinstance(name, str) or name == '' or not mgr or not event:
        return -1
    if name == 'ccsConfigured':
        return mgr.getEvent_ccsConfigured(event)
    elif name == 'endInitializeGuider':
        return mgr.getEvent_endInitializeGuider(event)
    elif name == 'endInitializeImage':
        return mgr.getEvent_endInitializeImage(event)
    elif name == 'endLoadFilter':
        return mgr.getEvent_endLoadFilter(event)
    elif name == 'endReadout':
        return mgr.getEvent_endReadout(event)
    elif name == 'endRotateCarousel':
        return mgr.getEvent_endRotateCarousel(event)
    elif name == 'endSetFilter':
        return mgr.getEvent_endSetFilter(event)
    elif name == 'endShutterClose':
        return mgr.getEvent_endShutterClose(event)
    elif name == 'endShutterOpen':
        return mgr.getEvent_endShutterOpen(event)
    elif name == 'endTakeImage':
        return mgr.getEvent_endTakeImage(event)
    elif name == 'endUnloadFilter':
        return mgr.getEvent_endUnloadFilter(event)
    elif name == 'notReadyToTakeImage':
        return mgr.getEvent_notReadyToTakeImage(event)
    elif name == 'prepareToTakeImage':
        return mgr.getEvent_prepareToTakeImage(event)
    elif name == 'readyToTakeImage':
        return mgr.getEvent_readyToTakeImage(event)
    elif name == 'startIntegration':
        return mgr.getEvent_startIntegration(event)
    elif name == 'startLoadFilter':
        return mgr.getEvent_startLoadFilter(event)
    elif name == 'startReadout':
        return mgr.getEvent_startReadout(event)
    elif name == 'startRotateCarousel':
        return mgr.getEvent_startRotateCarousel(event)
    elif name == 'startSetFilter':
        return mgr.getEvent_startSetFilter(event)
    elif name == 'startShutterClose':
        return mgr.getEvent_startShutterClose(event)
    elif name == 'startShutterOpen':
        return mgr.getEvent_startShutterOpen(event)
    elif name == 'startUnloadFilter':
        return mgr.getEvent_startUnloadFilter(event)
    else:
        return -1


# +
# function: event_reponse()
# -
def event_response(name='', event=None):
    if not isinstance(name, str) or name == '' or not event:
        return ''
    if name == 'ccsConfigured':
        return ''
    elif name == 'endInitializeGuider':
        return ''
    elif name == 'endInitializeImage':
        return ''
    elif name == 'endLoadFilter':
        return ''
    elif name == 'endReadout':
        return ''
    elif name == 'endRotateCarousel':
        return ''
    elif name == 'endSetFilter':
        return ''
    elif name == 'endShutterClose':
        return ''
    elif name == 'endShutterOpen':
        return ''
    elif name == 'endTakeImage':
        return ''
    elif name == 'endUnloadFilter':
        return ''
    elif name == 'notReadyToTakeImage':
        return ''
    elif name == 'prepareToTakeImage':
        return ''
    elif name == 'readyToTakeImage':
        return ''
    elif name == 'startIntegration':
        return '\tevent.imageName = {0:s}'.format(event.imageName)
    elif name == 'startLoadFilter':
        return ''
    elif name == 'startReadout':
        return ''
    elif name == 'startRotateCarousel':
        return ''
    elif name == 'startSetFilter':
        return ''
    elif name == 'startShutterClose':
        return ''
    elif name == 'startShutterOpen':
        return ''
    elif name == 'startUnloadFilter':
        return ''
    else:
        return ''


# +
# main()
# -
if __name__ == "__main__":

    # list of events
    events = ['ccsConfigured', 'endInitializeGuider', 'endInitializeImage', 'endLoadFilter',
              'endReadout', 'endRotateCarousel', 'endSetFilter', 'endShutterClose', 'endShutterOpen',
              'endTakeImage', 'endUnloadFilter', 'notReadyToTakeImage', 'prepareToTakeImage', 'readyToTakeImage',
              'startIntegration', 'startLoadFilter', 'startReadout', 'startRotateCarousel', 'startSetFilter',
              'startShutterClose', 'startShutterOpen', 'startUnloadFilter']

    # create threads for each event:
    threads = []
    for T in events:
        t = threading.Thread(name=T, target=thread_code)
        threads.append(t)
        t.start()
