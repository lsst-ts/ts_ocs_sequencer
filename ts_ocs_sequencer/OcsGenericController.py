#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from __future__ import print_function
import signal
from OcsEvents import *
from OcsStates import *


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
# function: service_shutdown()
# -
def service_shutdown(signum=0, frame=None):
    raise ServiceExit


# +
# class: ServiceExit() inherits from Exception
# -
class ServiceExit(Exception):
    pass


# +
# class: Worker() inherits from threading.Thread
# -
class Worker(threading.Thread):

    # +
    # __init__
    # -
    def __init__(self, nam='', ent='', evh=None, smc=None):

        # __init__ the superclass
        threading.Thread.__init__(self)

        # save input(s)
        self._name = nam
        self._entity = ent
        self._evh = evh
        self._smc = smc

        # check input(s)
        if not isinstance(self._name, str) or self._name == '':
            raise ServiceExit
        if not isinstance(self._entity, str) or self._entity == '':
            raise ServiceExit

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None

        self._cmdid = None
        self._commands = None
        self._configs = None
        self._container = None
        self._cstate = None
        self._entity_lc = self._entity.lower()
        self._log = None
        self._ocsid = None
        self._pid = os.getpid()
        self._processor = None
        self._pstate = None
        self._retval = None

        self.shutdown_flag = None

        # get state information
        self._summ = ocsEntitySummaryState
        self._cmds = ocsEntitySummaryStateCommands
        self._cfgs = ocsEntitySummaryStateConfigurations
        self._cfgs[OCS_SUMMARY_STATE_STANDBY] = ['{0:s}-Normal'.format(self._entity)]

        if self._evh:
            self._evh.logger.info('{0:s} {1:s} thread event handler at address {1:s}'.format(
                self._entity, self._name, hex(id(self._evh))))
        if self._smc:
            self._smc.logger.info('{0:s} {1:s} thread state machine at address {1:s}'.format(
                self._entity, self._name, hex(id(self._smc))))

    # +
    # (hidden) method: _setup_processor()
    # -
    def _setup_processor(self):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} entry'.format(
            self._entity, self._name, str(self._processor)))

        # get processor according to command
        try:
            sobj = ocs_sal_attribute(self.__mgr, 'salProcessor')
            self._processor = sobj('{0:s}_command_{1:s}'.format(self._entity_lc, self._name))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} exit'.format(
            self._entity, self._name, str(self._processor)))

    # +
    # (hidden) method: _get_container()
    # -
    def _get_container(self):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} entry'.format(
            self._entity, self._name, str(self._container)))

        # get payload container
        try:
            sobj = ocs_sal_attribute(self.__sal, '{0:s}_command_{1:s}C'.format(self._entity_lc, self._name))
            self._container = sobj()
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} exit'.format(
            self._entity, self._name, str(self._container)))

    # +
    # (hidden) method: _accept_command()
    # -
    def _accept_command(self):

        # entry message
        # self._log.logger.info('{0:s} {1:s} thread _accept_command()={2:s} entry'.format(
        #     self._entity, self._name, str(self._cmdid)))

        # accept command
        try:
            sobj = ocs_sal_attribute(self.__mgr, 'acceptCommand_{0:s}'.format(self._name))
            self._cmdid = sobj(self._container)
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self._cmdid = -1

        # exit message
        # self._log.logger.info('{0:s} {1:s} thread _accept_command()={2:s} exit'.format(
        #     self._entity, self._name, str(self._cmdid)))

    # +
    # (hidden) method: _ack_command()
    # -
    def _ack_command(self, code=0, msg=''):

        # entry message
        self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} entry'.format(
            self._entity, self._name, str(self._retval)))

        # acknowledge command
        try:
            sobj = ocs_sal_attribute(self.__mgr, 'ackCommand_{0:s}'.format(self._name))
            self._retval = sobj(self._cmdid, code, 0, msg)
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self._retval = -1

        # exit message
        self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} exit'.format(
            self._entity, self._name, str(self._retval)))

    # +
    # (hidden) method: _process_command()
    # -
    def _process_command(self):

        # set state machine to busy
        self._smc.setBusy = True

        # acknowledge the command
        self._ack_command(SAL__CMD_INPROGRESS, 'Ack : OK')

        # get state information
        current_state = self._smc.current_state
        previous_state = self._smc.previous_state
        self._cstate = self._summ.get(current_state, '')
        self._pstate = self._summ.get(previous_state, '')
        self._commands = self._cmds.get(current_state, [])
        self._configs = self._cfgs.get(current_state, [])
        self._ocsid = ocs_id(False)

        # does the state support this command?
        if self._name not in self._commands:
            self._ack_command(SAL__CMD_FAILED, 'Error : Command disallowed in {0:s} state'.format(
                ocsEntitySummaryState.get(current_state, '')))
            return

        # do state change
        else:

            # generate a state change event
            sal_event = '{0:s}EntitySummaryState'.format(self._entity_lc)
            self._evh.send_event(sal_event,
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

            # change state
            if self._name == 'abort':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_FAULT)
            elif self._name == 'disable':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_DISABLED)
            elif self._name == 'enable':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_ENABLED)
            elif self._name == 'enterControl':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_STANDBY)
            elif self._name == 'exitControl':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_OFFLINE)
            elif self._name == 'setValue':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_ENABLED)
            elif self._name == 'standby':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_STANDBY)
            elif self._name == 'start':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_DISABLED)
            elif self._name == 'stop':
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_ENABLED)

            # done
            self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

        # set state machine to not busy
        self._smc.setBusy = False

    # +
    # (hidden) method: _dump_payload()
    # -
    def _dump_payload(self):

        # dump payload
        if self._name == 'abort':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'disable':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'enable':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'enterControl':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'exitControl':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'setValue':
            self._log.logger.info('{0:s} {1:s} thread payload parameter={2:s} value={3:s}'.format(
                self._entity, self._name, str(self._container.parameter), str(self._container.value)))
        elif self._name == 'standby':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))
        elif self._name == 'start':
            self._log.logger.info('{0:s} {1:s} thread payload configuration={2:s}'.format(
                self._entity, self._name, str(self._container.configuration)))
        elif self._name == 'stop':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.state)))

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
        try:
            self._log.logger.info('{0:s} {1:s} thread importing SALPY_{2:s}'.format(
                self._entity, self._name, self._entity_lc))
            self.__sal = ocs_sal_import('SALPY_{0:s}'.format(self._entity_lc))
            self._log.logger.info('{0:s} {1:s} thread imported SALPY_{2:s} OK'.format(
                self._entity, self._name, self._entity_lc))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

        # get self.__mgr object (cf. mgr = SAL_archiver())
        try:
            self._log.logger.info('{0:s} {1:s} thread get attribute SAL_{2:s}'.format(
                self._entity, self._name, self._entity_lc))
            sobj = ocs_sal_attribute(self.__sal, 'SAL_{0:s}'.format(self._entity_lc))
            self.__mgr = sobj()
            self._log.logger.info('{0:s} {1:s} thread got attribute SAL_{2:s} OK'.format(
                self._entity, self._name, self._entity_lc))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

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
    except IndexError:
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
        for T in ['abort', 'disable', 'enable', 'enterControl', 'exitControl', 'standby', 'start', 'stop']:
            t = Worker(T, entity, event_processor, state_machine)
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
