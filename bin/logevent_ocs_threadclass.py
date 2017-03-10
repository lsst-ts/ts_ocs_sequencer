#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import threading
import time
import signal
from ocs_sal import *
from OcsLogger import *


# +
# __doc__ string
# -
__doc__ = """Event logger for events in the OCS (using a thread class)"""


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
# Exception: ServiceExit
# - 
class ServiceExit(Exception):
    pass


# +
# function: service_shutdown()
# - 
def service_shutdown(signum, frame):
    print('signum={0:s}'.format(str(signum)))
    print('frame={0:s}'.format(str(frame)))
    raise ServiceExit

 
# +
# function: Worker()
# -
class Worker(threading.Thread):

    # +
    # __init__
    # - 
    def __init__(self, name=''):

        # __init__ the superclass
        threading.Thread.__init__(self)
 
        # check input(s)
        self.name = name
        if not isinstance(self.name, str) or self.name == '':
            self.name = '{0:s}-{0:d}'.format(os.getenv('USER'), os.getpid())

        # shutdown_flag is a threading.Event object that indicates whether the thread should be terminated
        self.shutdown_flag = threading.Event()
 
        # get logger
        self.evlog = OcsLogger('Events', self.name)
        self.evlog.logger.info('{0:s} thread starting up'.format(self.name))

        # import the SAL component (cf. from SALPY_ocs import *)
        self.evlog.logger.info('Importing SALPY_ocs')
        try:
            self.__sal = ocs_sal_import('SALPY_ocs')
        except OcsGenericEntityException as e:
            self.evlog.logger.error(e.errstr)
            return
        if self.__sal:
            self.evlog.logger.info('Imported SALPY_ocs OK')

        # get mgr object (cf. mgr = SAL_ocs())
        self.evlog.logger.debug('Getting attribute SAL_ocs')
        try:
            self.__mgr = ocs_sal_attribute(self.__sal, 'SAL_ocs')
        except OcsGenericEntityException as e:
            self.evlog.logger.error(e.errstr)
            return
        if self.__mgr:
            self.__mgr = self.__mgr()
        self.evlog.logger.debug('Got attribute SAL_ocs OK')

    # +
    # method: run()
    # - 
    def run(self):

        # entry message
        self.evlog.logger.info('{0:s} thread starting'.format(self.name))
        self.__mgr.salEvent('ocs_logevent_{0:s}'.format(self.name))

        # get container
        if self.name == 'ocsCommandIssued':
            event = self.__sal.ocs_logevent_ocsCommandIssuedC()
        elif self.name == 'ocsCommandStatus':
            event = self.__sal.ocs_logevent_ocsCommandStatusC()
        elif self.name == 'ocsEntityShutdown':
            event = self.__sal.ocs_logevent_ocsEntityShutdownC()
        elif self.name == 'ocsEntityStartup':
            event = self.__sal.ocs_logevent_ocsEntityStartupC()
        elif self.name == 'ocsEntitySummaryState':
            event = self.__sal.ocs_logevent_ocsEntitySummaryStateC()
        else:
            event = None
        self.evlog.logger.info('{0:s} thread container created'.format(self.name))

        # loop until signal arrives from main thread
        while not self.shutdown_flag.is_set():

            # get event
            if self.name == 'ocsCommandIssued':
                retval = self.__mgr.getEvent_ocsCommandIssued(event)
            elif self.name == 'ocsCommandStatus':
                retval = self.__mgr.getEvent_ocsCommandStatus(event)
            elif self.name == 'ocsEntityShutdown':
                retval = self.__mgr.getEvent_ocsEntityShutdown(event)
            elif self.name == 'ocsEntityStartup':
                retval = self.__mgr.getEvent_ocsEntityStartup(event)
            elif self.name == 'ocsEntitySummaryState':
                retval = self.__mgr.getEvent_ocsEntitySummaryState(event)
            else:
                retval = -1

            # event received so report payload
            if retval == 0:
                self.evlog.logger.info('{0:s} thread event received'.format(self.name))
                if self.name == 'ocsCommandIssued':
                    self.evlog.logger.info(
                        '\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
                    self.evlog.logger.info(
                        '\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
                    self.evlog.logger.info(
                        '\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority       = {0:d}'.format(event.priority))
                    self.evlog.logger.info(
                        '\tevent.ReturnValue    = {0:d}'.format(event.ReturnValue))
                    self.evlog.logger.info(
                        '\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
                    self.evlog.logger.info(
                        '\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
                elif self.name == 'ocsCommandStatus':
                    self.evlog.logger.info(
                        '\tevent.CommandSource  = {0:s}'.format(event.CommandSource))
                    self.evlog.logger.info(
                        '\tevent.CommandSent    = {0:s}'.format(event.CommandSent))
                    self.evlog.logger.info(
                        '\tevent.Identifier     = {0:.17f}'.format(event.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority       = {0:d}'.format(event.priority))
                    self.evlog.logger.info(
                        '\tevent.SequenceNumber = {0:d}'.format(event.SequenceNumber))
                    self.evlog.logger.info(
                        '\tevent.Status         = {0:s}'.format(event.Status))
                    self.evlog.logger.info(
                        '\tevent.StatusValue    = {0:d}'.format(event.StatusValue))
                    self.evlog.logger.info(
                        '\tevent.Timestamp      = {0:s}'.format(event.Timestamp))
                elif self.name == 'ocsEntityShutdown':
                    self.evlog.logger.info(
                        '\tevent.Address    = {0:d}'.format(event.Address))
                    self.evlog.logger.info(
                        '\tevent.Identifier = {0:.17f}'.format(event.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority   = {0:d}'.format(event.priority))
                    self.evlog.logger.info(
                        '\tevent.Name       = {0:s}'.format(event.Name))
                    self.evlog.logger.info(
                        '\tevent.Timestamp  = {0:s}'.format(event.Timestamp))
                elif self.name == 'ocsEntityStartup':
                    self.evlog.logger.info(
                        '\tevent.Address    = {0:d}'.format(event.Address))
                    self.evlog.logger.info(
                        '\tevent.Name       = {0:s}'.format(event.Name))
                    self.evlog.logger.info(
                        '\tevent.priority   = {0:d}'.format(event.priority))
                    self.evlog.logger.info(
                        '\tevent.Identifier = {0:.17f}'.format(event.Identifier))
                    self.evlog.logger.info(
                        '\tevent.Timestamp  = {0:s}'.format(event.Timestamp))
                elif self.name == 'ocsEntitySummaryState':
                    self.evlog.logger.info(
                        '\tevent.Address                 = {0:d}'.format(event.Address))
                    self.evlog.logger.info(
                        '\tevent.CommandsAvailable       = {0:s}'.format(event.CommandsAvailable))
                    self.evlog.logger.info(
                        '\tevent.ConfigurationsAvailable = {0:s}'.format(event.ConfigurationsAvailable))
                    self.evlog.logger.info(
                        '\tevent.Executing               = {0:s}'.format(event.Executing))
                    self.evlog.logger.info(
                        '\tevent.Identifier              = {0:.17f}'.format(event.Identifier))
                    self.evlog.logger.info(
                        '\tevent.Name                    = {0:s}'.format(event.Name))
                    self.evlog.logger.info(
                        '\tevent.CurrentState            = {0:s}'.format(event.CurrentState))
                    self.evlog.logger.info(
                        '\tevent.PreviousState           = {0:s}'.format(event.PreviousState))
                    self.evlog.logger.info(
                        '\tevent.priority                = {0:d}'.format(event.priority))
                    self.evlog.logger.info(
                        '\tevent.Timestamp               = {0:s}'.format(event.Timestamp))
                else:
                    pass
            time.sleep(1)

        # exit message
        self.__mgr.salShutdown()
        self.evlog.logger.info('thread {0:s} shutting down'.format(self.name))


# +
# main()
# -
if __name__ == "__main__":

    # register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
 
    # start main and worker threads
    threads = []
    try:
        # create threads for each event:
        for T in ['ocsCommandIssued', 'ocsCommandStatus', 'ocsEntityShutdown',
                  'ocsEntityStartup', 'ocsEntitySummaryState']:
            t = Worker(T)
            threads.append(t)
            t.start()

        # keep the main thread running, otherwise signals are ignored
        while True:
            time.sleep(1)
 
    except ServiceExit:
        # set flag in threads
        for t in threads:
            t.shutdown_flag.set()
        # wait for flags to exit
        for t in threads:
            t.join()
