#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from __future__ import print_function
import argparse
import signal
import sys
import threading
import time
from ocs_common import *
from OcsEvents import *
from OcsLogger import *
from OcsStates import *
from SALPY_archiver import *


# +
# __doc__ string
# -
__doc__ = """Controller for generic commandable entity"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "7 March 2017"
__email__ = "pdaly@lsst.org"
__file__ = "OcsGenericController.py"
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
# class: Worker()
# -
class Worker(threading.Thread):

    # +
    # __init__
    # - 
    def __init__(self, name='', entity='', evh=None, smc=None):

        # __init__ the superclass
        threading.Thread.__init__(self)
 
        # save input(s)
        self._name = name.lower()
        self._entity = entity.lower()
        self._evh = evh
        self._smc = smc

        # check input(s)
        if not isinstance(self._name, str) or self._name == '':
            self._name = '{0:s}-{0:d}'.format(os.getenv('USER'), os.getpid()).lower()
        if not isinstance(self._entity, str) or self._entity == '':
            self._entity = 'Test'.lower()

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None
        self._cmdid = None
        self._commands = None
        self._configs = None
        self._container = None
        self._cstate = None
        self._log = None
        self._ocsid = None
        self._pid = os.getpid()
        self._processor = None
        self._pstate = None
        self._retval = None

        # get state information
        self._summ = ocsEntitySummaryState
        self._cmds = ocsEntitySummaryStateCommands
        self._cfgs = ocsEntitySummaryStateConfigurations
        self._cfgs[OCS_SUMMARY_STATE_STANDBY] = ['{0:s}-Normal'.format(self._entity)]

        if self._evh:
            self._evh.logger.info('{0:s} {1:s} thread event handler at address {1:s}'.format(self._entity, self._name, hex(id(self._evh))))
        if self._smc:
            self._smc.logger.info('{0:s} {1:s} thread state machine at address {1:s}'.format(self._entity, self._name, hex(id(self._smc))))

    # +
    # (hidden) method: _setup_processor()
    # - 
    def _setup_processor(self):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} entry'.format(self._entity, self._name, str(self._processor)))

        # get processor according to command
        if self._name == 'abort':
            self._processor = self.__mgr.salProcessor('archiver_command_abort')
        elif self._name == 'disable':
            self._processor = self.__mgr.salProcessor('archiver_command_disable')
        elif self._name == 'enable':
            self._processor = self.__mgr.salProcessor('archiver_command_enable')
        elif self._name == 'entercontrol':
            self._processor = self.__mgr.salProcessor('archiver_command_enterControl')
        elif self._name == 'exitcontrol':
            self._processor = self.__mgr.salProcessor('archiver_command_exitControl')
        #elif self._name == 'setvalue':
        #    self._processor = self.__mgr.salProcessor('archiver_command_setValue')
        elif self._name == 'standby':
            self._processor = self.__mgr.salProcessor('archiver_command_standby')
        elif self._name == 'start':
            self._processor = self.__mgr.salProcessor('archiver_command_start')
        elif self._name == 'stop':
            self._processor = self.__mgr.salProcessor('archiver_command_stop')
        else:
            self._processor = None

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} exit'.format(self._entity, self._name, str(self._processor)))

    # +
    # (hidden) method: _get_container()
    # - 
    def _get_container(self):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} entry'.format(self._entity, self._name, str(self._container)))
    
        # get payload container
        if self._name == 'abort':
            self._container = archiver_command_abortC()
        elif self._name == 'disable':
            self._container = archiver_command_disableC()
        elif self._name == 'enable':
            self._container = archiver_command_enableC()
        elif self._name == 'entercontrol':
            self._container = archiver_command_enterControlC()
        elif self._name == 'exitcontrol':
            self._container = archiver_command_exitControlC()
        #elif self._name == 'setvalue':
        #    self._container = archiver_command_setValueC()
        elif self._name == 'standby':
            self._container = archiver_command_standbyC()
        elif self._name == 'start':
            self._container = archiver_command_startC()
        elif self._name == 'stop':
            self._container = archiver_command_stopC()
        else:
            self._container = None

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} exit'.format(self._entity, self._name, str(self._container)))

    # +
    # (hidden) method: _accept_command()
    # - 
    def _accept_command(self):

        # entry message
        # self._log.logger.info('{0:s} {1:s} thread _accept_command()={2:s} entry'.format(self._entity, self._name, str(self._cmdid)))
    
        # accept command
        if self._name == 'abort':
            self._cmdid = self.__mgr.acceptCommand_abort(self._container)
        elif self._name == 'disable':
            self._cmdid = self.__mgr.acceptCommand_disable(self._container)
        elif self._name == 'enable':
            self._cmdid = self.__mgr.acceptCommand_enable(self._container)
        elif self._name == 'entercontrol':
            self._cmdid = self.__mgr.acceptCommand_enterControl(self._container)
        elif self._name == 'exitcontrol':
            self._cmdid = self.__mgr.acceptCommand_exitControl(self._container)
        #elif self._name == 'setvalue':
        #    self._cmdid = self.__mgr.acceptCommand_setValue(self._container)
        elif self._name == 'standby':
            self._cmdid = self.__mgr.acceptCommand_standby(self._container)
        elif self._name == 'start':
            self._cmdid = self.__mgr.acceptCommand_start(self._container)
        elif self._name == 'stop':
            self._cmdid = self.__mgr.acceptCommand_stop(self._container)
        else:
            self._cmdid = -1

        # exit message
        # self._log.logger.info('{0:s} {1:s} thread _accept_command()={2:s} exit'.format(self._entity, self._name, str(self._cmdid)))

    # +
    # (hidden) method: _ack_command()
    # - 
    def _ack_command(self, code=0, msg=''):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} entry'.format(self._entity, self._name, str(self._retval)))
   
        # acknowledge command
        if self._name == 'abort':
            self._retval = self.__mgr.ackCommand_abort(self._cmdid, code, 0, msg)
        elif self._name == 'disable':
            self._retval = self.__mgr.ackCommand_disable(self._cmdid, code, 0, msg)
        elif self._name == 'enable':
            self._retval = self.__mgr.ackCommand_enable(self._cmdid, code, 0, msg)
        elif self._name == 'entercontrol':
            self._retval = self.__mgr.ackCommand_enterControl(self._cmdid, code, 0, msg)
        elif self._name == 'exitcontrol':
            self._retval = self.__mgr.ackCommand_exitControl(self._cmdid, code, 0, msg)
        #elif self._name == 'setvalue':
        #   self._retval = self.__mgr.ackCommand_setValue(self._cmdid, code, 0, msg)
        elif self._name == 'standby':
            self._retval = self.__mgr.ackCommand_standby(self._cmdid, code, 0, msg)
        elif self._name == 'start':
            self._retval = self.__mgr.ackCommand_start(self._cmdid, code, 0, msg)
        elif self._name == 'stop':
            self._retval = self.__mgr.ackCommand_stop(self._cmdid, code, 0, msg)
        else:
            self_retval = -1

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} exit'.format(self._entity, self._name, str(self._retval)))

    # +
    # (hidden) method: _process_command()
    # - 
    def _process_command(self):

        # set state machine to busy
        self._smc.setBusy = True

        # acknowledge the command
        self._ack_command(SAL__CMD_INPROGRESS, 'Ack : OK')

        # get state information
        self._cstate = self._summ.get(self._smc._current_state, '')
        self._pstate = self._summ.get(self._smc._previous_state, '')
        self._commands = self._cmds.get(self._smc._current_state, [])
        self._configs = self._cfgs.get(self._smc._current_state, [])
        self._ocsid = ocs_id(False)

        # does the state support this command?
        if self._name not in self._commands:
            self._ack_command(SAL__CMD_FAILED, 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(self._smc._current_state, '')))
            return

        # do state change
        else:

            # generate a state change event
            self._evh.send_event('archiverEntitySummaryState',
                Name=self._entity,
                CurrentState=str(self._cstate),
                PreviousState=str(self._pstate),
                Identifier=self._ocsid,
                Timestamp=ocs_mjd_to_iso(self._ocsid),
                Executing=self._name,
                Address=self._pid,
                CommandsAvailable=str(self._commands),
                ConfigurationsAvailable=str(self._configs),
                priority=SAL__EVENT_INFO)

            if self._name == 'abort':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_FAULT)
            elif self._name == 'disable':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_DISABLED)
            elif self._name == 'enable':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_ENABLED)
            elif self._name == 'entercontrol':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_STANDBY)
            elif self._name == 'exitcontrol':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_OFFLINE)
            elif self._name == 'setvalue':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_ENABLED)
            elif self._name == 'standby':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_STANDBY)
            elif self._name == 'start':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_DISABLED)
            elif self._name == 'stop':
                self._smc.change_state(self._smc._current_state, OCS_SUMMARY_STATE_ENABLED)

            self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

        # set state machine to not busy
        self._smc.setBusy = False

    # +
    # (hidden) method: _dump_payload()
    # - 
    def _dump_payload(self):
    
        # dump payload
        if self._name == 'abort':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        elif self._name == 'disable':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        elif self._name == 'enable':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        elif self._name == 'entercontrol':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        elif self._name == 'exitcontrol':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        #elif self._name == 'setvalue':
        #   self._log.logger.info('{0:s} {1:s} thread payload parameter={2:s} value={3:s}'.format(self._entity, self._name, 
        #       str(self._container.parameter), str(self._contianer.value)))
        elif self._name == 'standby':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))
        elif self._name == 'start':
            self._log.logger.info('{0:s} {1:s} thread payload configuration={2:s}'.format(self._entity, self._name, str(self._container.configuration)))
        elif self._name == 'stop':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(self._entity, self._name, str(self._container.state)))

    # +
    # method: run()
    # - 
    def run(self):

        # shutdown_flag is a threading.Event object that indicates whether the thread should be terminated
        self.shutdown_flag = threading.Event()
 
        # set up logging
        self._log = OcsLogger(self._entity, self._name)
        self._log.logger.info('{0:s} {1:s} thread starting up'.format(self._entity, self._name))

        # get self.__sal object (cf. from SALPY_archiver import *)
        self._log.logger.info('{0:s} {1:s} thread importing SALPY_{2:s}'.format(self._entity, self._name, self._entity))
        try:
            self.__sal = ocs_sal_import('SALPY_{0:s}'.format(self._entity))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            return
        self._log.logger.info('{0:s} {1:s} thread imported SALPY_{2:s} OK'.format(self._entity, self._name, self._entity))

        # get self.__mgr object (cf. mgr = SAL_archiver())
        self._log.logger.info('{0:s} {1:s} thread get attribute SAL_{2:s}'.format(self._entity, self._name, self._entity))
        try:
            self.__mgr = ocs_sal_attribute(self.__sal, 'SAL_{0:s}'.format(self._entity))
            self.__mgr = self.__mgr()
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            return
        self._log.logger.info('{0:s} {1:s} thread got attribute SAL_{2:s} OK'.format(self._entity, self._name, self._entity))

        # set up command processor
        self._setup_processor()

        # set up payload container
        self._get_container()

        # loop until signal arrives from main thread
        self._log.logger.info('{0:s} {1:s} thread entering loop'.format(self._entity, self._name))
        while not self.shutdown_flag.is_set():

            # accept a command
            self._accept_command()

            # process the command
            if self._cmdid > 0:
                self._log.logger.info('{0:s} thread command identifier {1:d}'.format(self._name, self._cmdid))

                # dump the payload
                self._dump_payload()

                # do something
                self._process_command()

            # this sleep means it's really polling?!
            time.sleep(1)

        # exit message
        self.__mgr.salShutdown()
        self._log.logger.info('thread {0:s} shutting down'.format(self._name))

# +
# main()
# -
if __name__ == "__main__":


    # get command line argument
    try:
        entity = str(sys.argv[1])
    except:
        entity = 'Test'

    # register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
 
    # created shared entities
    event_processor = OcsEvents(False)
    state_machine = OcsStates()

    # set up state machine
    if state_machine:
        state_machine.change_state(OCS_SUMMARY_STATE_UNKNOWN, OCS_SUMMARY_STATE_OFFLINE)

    # start main and worker threads
    threads = []
    try:
        # create threads for each command:
        for T in [ 'abort', 'disable', 'enable', 'enterControl', 'exitControl', 'standby', 'start', 'stop']:
            t=Worker(T, entity, event_processor, state_machine)
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
