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
__doc__ = """Event logger for events in the OCS sequencer (using a thread class)"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "17 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "logevent_sequencer_threadclass.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"

 
# +
# function: service_shutdown()
# - 
def service_shutdown(signum, frame):
    raise ServiceExit

 
# +
# Exception: ServiceExit
# - 
class ServiceExit(Exception):
    pass


# +
# function: Worker()
# -
class Worker(threading.Thread):

    # +
    # __init__
    # - 
    def __init__(self, name='', entity=''):

        # __init__ the superclass
        threading.Thread.__init__(self)
 
        # get input(s)
        self._name = name
        self._entity = entity

        # shutdown_flag is a threading.Event object that indicates whether the thread should be terminated
        self.shutdown_flag = threading.Event()
 
        # check input(s)
        if not isinstance(self._name, str) or self._name == '':
            self.shutdown_flag.set()
        if not isinstance(self._entity, str) or self._entity == '':
            self.shutdown_flag.set()

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None
 
        self._container = None
        self._entity_lc = self._entity.lower()
        self._retval = None

        # get logger
        self.evlog = OcsLogger(self._entity, self._name)
        self.evlog.logger.info('{0:s} {1:s} thread starting up'.format(self._entity, self._name))

    # +
    # (hidden) method: _get_sal_connection()
    # (cf. from SALPY_xxx import *)
    # -
    def _get_sal_connection(self):
        try:
            self.evlog.logger.info('Importing SALPY_{0:s}'.format(self._entity_lc))
            self.__sal = ocs_sal_import('SALPY_{0:s}'.format(self._entity_lc))
            if self.__sal:
                self.evlog.logger.info('Imported SALPY_{0:s} OK'.format(self._entity_lc))
        except OcsGenericEntityException as e:
            self.evlog.logger.error(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _get_mgr_connection()
    # (cf. mgr = SAL_xxx())
    # -
    def _get_mgr_connection(self):
        try:
            self.evlog.logger.info('Getting attribute SAL_{0:s}'.format(self._entity_lc))
            self.__mgr = ocs_sal_attribute(self.__sal, 'SAL_{0:s}'.format(self._entity_lc))
            if self.__mgr:
                self.__mgr = self.__mgr()
                self.evlog.logger.info('Got attribute SAL_{0:s} OK'.format(self._entity_lc))
        except OcsGenericEntityException as e:
            self.evlog.logger.error(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _get_container()
    # -
    def _get_container(self):
        try:
            self.evlog.logger.info('{0:s} {1:s} thread _get_container()={2:s} entry'.format(
                self._entity, self._name, str(self._container)))
            sobj = ocs_sal_attribute(self.__sal, '{0:s}_logevent_{1:s}C'.format(self._entity_lc, self._name))
            self._container = sobj()
            self.evlog.logger.info('{0:s} {1:s} thread _get_container()={2:s} exit'.format(
                self._entity, self._name, str(self._container)))
        except OcsGenericEntityException as e:
            self.evlog.logger.critical(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _get_event()
    # -
    def _get_event(self):
        try:
            sobj = ocs_sal_attribute(self.__mgr, 'getEvent_{0:s}'.format(self._name))
            self._retval = sobj(self._container)
        except OcsGenericEntityException as e:
            self.evlog.logger.critical(e.errstr)
            self._retval = -1

    # +
    # method: run()
    # - 
    def run(self):

        # entry message
        self.evlog.logger.info('{0:s} {1:s} thread starting'.format(self._entity, self._name))

        # connect to sal and set up for this event
        self._get_sal_connection()
        self._get_mgr_connection()
        self.__mgr.salEvent('{0:s}_logevent_{1:s}'.format(self._entity_lc, self._name))

        # get container
        self._get_container()
        if not self._container:
            self.shutdown_flag.set()
        self.evlog.logger.info('{0:s} {1:s} thread container created'.format(self._entity, self._name))

        # loop until signal arrives from main thread
        while not self.shutdown_flag.is_set():

            # get event
            self._get_event()
            #self.evlog.logger.info('{0:s} {1:s} thread retval received {2:s}'.format(self._entity, self._name, str(self._retval)))

            # event received so report payload
            if self._retval == 0:
                self.evlog.logger.info('{0:s} {1:s} thread event received'.format(self._entity, self._name))

                if self._name.find('{0:s}CommandIssued'.format(self._entity_lc)) >= 0:
                    self.evlog.logger.info(
                        '\tevent.CommandSent    = {0:s}'.format(self._container.CommandSent))
                    self.evlog.logger.info(
                        '\tevent.CommandSource  = {0:s}'.format(self._container.CommandSource))
                    self.evlog.logger.info(
                        '\tevent.Identifier     = {0:.17f}'.format(self._container.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority       = {0:d}'.format(self._container.priority))
                    self.evlog.logger.info(
                        '\tevent.ReturnValue    = {0:d}'.format(self._container.ReturnValue))
                    self.evlog.logger.info(
                        '\tevent.SequenceNumber = {0:d}'.format(self._container.SequenceNumber))
                    self.evlog.logger.info(
                        '\tevent.Timestamp      = {0:s}'.format(self._container.Timestamp))

                elif self._name.find('{0:s}CommandStatus'.format(self._entity_lc)) >= 0:
                    self.evlog.logger.info(
                        '\tevent.CommandSource  = {0:s}'.format(self._container.CommandSource))
                    self.evlog.logger.info(
                        '\tevent.CommandSent    = {0:s}'.format(self._container.CommandSent))
                    self.evlog.logger.info(
                        '\tevent.Identifier     = {0:.17f}'.format(self._container.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority       = {0:d}'.format(self._container.priority))
                    self.evlog.logger.info(
                        '\tevent.SequenceNumber = {0:d}'.format(self._container.SequenceNumber))
                    self.evlog.logger.info(
                        '\tevent.Status         = {0:s}'.format(self._container.Status))
                    self.evlog.logger.info(
                        '\tevent.StatusValue    = {0:d}'.format(self._container.StatusValue))
                    self.evlog.logger.info(
                        '\tevent.Timestamp      = {0:s}'.format(self._container.Timestamp))

                elif self._name.find('{0:s}EntityShutdown'.format(self._entity_lc)) >= 0:
                    self.evlog.logger.info(
                        '\tevent.Address    = {0:d}'.format(self._container.Address))
                    self.evlog.logger.info(
                        '\tevent.Identifier = {0:.17f}'.format(self._container.Identifier))
                    self.evlog.logger.info(
                        '\tevent.priority   = {0:d}'.format(self._container.priority))
                    self.evlog.logger.info(
                        '\tevent.Name       = {0:s}'.format(self._container.Name))
                    self.evlog.logger.info(
                        '\tevent.Timestamp  = {0:s}'.format(self._container.Timestamp))

                elif self._name.find('{0:s}EntityStartup'.format(self._entity_lc)) >= 0:
                    self.evlog.logger.info(
                        '\tevent.Address    = {0:d}'.format(self._container.Address))
                    self.evlog.logger.info(
                        '\tevent.Name       = {0:s}'.format(self._container.Name))
                    self.evlog.logger.info(
                        '\tevent.priority   = {0:d}'.format(self._container.priority))
                    self.evlog.logger.info(
                        '\tevent.Identifier = {0:.17f}'.format(self._container.Identifier))
                    self.evlog.logger.info(
                        '\tevent.Timestamp  = {0:s}'.format(self._container.Timestamp))

                elif self._name.find('{0:s}EntitySummaryState'.format(self._entity_lc)) >= 0:
                    self.evlog.logger.info(
                        '\tevent.Address                 = {0:d}'.format(self._container.Address))
                    self.evlog.logger.info(
                        '\tevent.CommandsAvailable       = {0:s}'.format(self._container.CommandsAvailable))
                    self.evlog.logger.info(
                        '\tevent.ConfigurationsAvailable = {0:s}'.format(self._container.ConfigurationsAvailable))
                    self.evlog.logger.info(
                        '\tevent.Executing               = {0:s}'.format(self._container.Executing))
                    self.evlog.logger.info(
                        '\tevent.Identifier              = {0:.17f}'.format(self._container.Identifier))
                    self.evlog.logger.info(
                        '\tevent.Name                    = {0:s}'.format(self._container.Name))
                    self.evlog.logger.info(
                        '\tevent.CurrentState            = {0:s}'.format(self._container.CurrentState))
                    self.evlog.logger.info(
                        '\tevent.PreviousState           = {0:s}'.format(self._container.PreviousState))
                    self.evlog.logger.info(
                        '\tevent.priority                = {0:d}'.format(self._container.priority))
                    self.evlog.logger.info(
                        '\tevent.Timestamp               = {0:s}'.format(self._container.Timestamp))

            # no valid event
            time.sleep(1)

        # exit message
        self.__mgr.salShutdown()
        self.evlog.logger.info('{0:s} {1:s} thread shutting down'.format(self._entity, self._name))


# +
# main()
# -
if __name__ == "__main__":

    # get command line argument
    try:
        entity = str(sys.argv[1])
    except IndexError:
        entity = 'Sequencer'
    entity_lc = entity.lower()

    # register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
 
    # start main and worker threads
    threads = []
    try:
        # create threads for each event:
        for T in ['{0:s}CommandIssued'.format(entity_lc),
                  '{0:s}CommandStatus'.format(entity_lc),
                  '{0:s}EntityShutdown'.format(entity_lc),
                  '{0:s}EntityStartup'.format(entity_lc),
                  '{0:s}EntitySummaryState'.format(entity_lc)]:
            t = Worker(T, entity)
            threads.append(t)
            t.start()

        # keep the main thread running, otherwise signals are ignored
        while True:
            time.sleep(1)
 
    except ServiceExit:
        # signal received so set flag in threads
        for t in threads:
            t.shutdown_flag.set()
        # wait for threads to exit
        for t in threads:
            t.join()
