#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from __future__ import print_function
import signal
from OcsEvents import *
from OcsStates import *
from OcsCameraEntity import *
from SALPY_sequencer import *

# +
# __doc__ string
# -
__doc__ = """Controller for Sequencer commandable entity"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "1 April 2017"
__email__ = "pdaly@lsst.org"
__file__ = "OcsSequencerController.py"
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
    def __init__(self, nam='', ent='', evh=None, smc=None, cam=None, tel=None, arc=None, cat=None, pro=None):

        # __init__ the superclass
        threading.Thread.__init__(self)

        # save input(s)
        self._name = nam
        self._entity = ent
        self._evh = evh
        self._smc = smc
        self._cam = cam
        self._tel = tel
        self._arc = arc
        self._cat = cat
        self._pro = pro

        # check input(s)
        if not isinstance(self._name, str) or self._name == '':
            raise ServiceExit
        if not isinstance(self._entity, str) or self._entity == '':
            raise ServiceExit

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None

        self._ackval = None
        self._cmdid = None
        self._cmde = None
        self._cmdr = None
        self._commands = None
        self._configs = None
        self._container = None
        self._cstate = None
        self._device = None
        self._entity_lc = self._entity.lower()
        self._indict = None
        self._log = None
        self._objd = None
        self._ocsid = None
        self._pid = os.getpid()
        self._processor = None
        self._pstate = None
        self._retval = None
        self._startid = None
        self._timeout = None

        self.shutdown_flag = None

        # get state information
        self._summ = ocsEntitySummaryState

        self._cmds = ocsEntitySummaryStateCommands
        if 'sequence' not in self._cmds[OCS_SUMMARY_STATE_ENABLED]:
            self._cmds[OCS_SUMMARY_STATE_ENABLED].append('sequence')
        if 'script' not in self._cmds[OCS_SUMMARY_STATE_ENABLED]:
            self._cmds[OCS_SUMMARY_STATE_ENABLED].append('script')

        self._cfgs = ocsEntitySummaryStateConfigurations
        self._cfgs[OCS_SUMMARY_STATE_STANDBY] = ['{0:s}-Normal'.format(self._entity)]

        if self._evh:
            self._evh.logger.info('{0:s} {1:s} thread event handler at address {2:s}'.format(
                self._entity, self._name, hex(id(self._evh))))
            self._evh.logger.info('{0:s} {1:s} thread states {2:s}'.format(
                self._entity, self._name, str(self._summ)))
            self._evh.logger.info('{0:s} {1:s} thread commands {2:s}'.format(
                self._entity, self._name, str(self._cmds)))
            self._evh.logger.info('{0:s} {1:s} thread configurations {2:s}'.format(
                self._entity, self._name, str(self._cfgs)))
        if self._smc:
            self._smc.logger.info('{0:s} {1:s} thread state machine at address {2:s}'.format(
                self._entity, self._name, hex(id(self._smc))))
        if self._cam:
            self._cam.logger.info('{0:s} {1:s} thread camera at address {2:s}'.format(
                self._entity, self._name, hex(id(self._cam))))
        if self._tel:
            self._tel.logger.info('{0:s} {1:s} thread tcs at address {2:s}'.format(
                self._entity, self._name, hex(id(self._tel))))
        if self._arc:
            self._arc.logger.info('{0:s} {1:s} thread archiver at address {2:s}'.format(
                self._entity, self._name, hex(id(self._arc))))
        if self._cat:
            self._cat.logger.info('{0:s} {1:s} thread catchup archiver at address {2:s}'.format(
                self._entity, self._name, hex(id(self._cat))))
        if self._pro:
            self._pro.logger.info('{0:s} {1:s} thread processing cluster at address {2:s}'.format(
                self._entity, self._name, hex(id(self._pro))))

    # +
    # (hidden) method: _get_sal_connection()
    # (cf. from SALPY_xxx import *)
    # -
    def _get_sal_connection(self):
        try:
            self._log.logger.info('Importing SALPY_{0:s}'.format(self._entity_lc))
            self.__sal = ocs_sal_import('SALPY_{0:s}'.format(self._entity_lc))
            if self.__sal:
                self._log.logger.info('Imported SALPY_{0:s} OK'.format(self._entity_lc))
        except OcsGenericEntityException as e:
            self._log.logger.error(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _get_mgr_connection()
    # (cf. mgr = SAL_xxx())
    # -
    def _get_mgr_connection(self):
        try:
            self._log.logger.debug('Getting attribute SAL_{0:s}'.format(self._entity_lc))
            self.__mgr = ocs_sal_attribute(self.__sal, 'SAL_{0:s}'.format(self._entity_lc))
            if self.__mgr:
                self.__mgr = self.__mgr()
                self._log.logger.debug('Got attribute SAL_{0:s} OK'.format(self._entity_lc))
        except OcsGenericEntityException as e:
            self._log.logger.error(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _setup_processor()
    # -
    def _setup_processor(self):
        try:
            self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} entry'.format(
                self._entity, self._name, str(self._processor)))
            sobj = ocs_sal_attribute(self.__mgr, 'salProcessor')
            self._processor = sobj('{0:s}_command_{1:s}'.format(self._entity_lc, self._name))
            self._log.logger.info('{0:s} {1:s} thread _setup_processor()={2:s} exit'.format(
                self._entity, self._name, str(self._processor)))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _get_container()
    # -
    def _get_container(self):
        try:
            self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} entry'.format(
                self._entity, self._name, str(self._container)))
            sobj = ocs_sal_attribute(self.__sal, '{0:s}_command_{1:s}C'.format(self._entity_lc, self._name))
            self._container = sobj()
            self._log.logger.info('{0:s} {1:s} thread _get_container()={2:s} exit'.format(
                self._entity, self._name, str(self._container)))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self.shutdown_flag.set()

    # +
    # (hidden) method: _accept_command()
    # -
    def _accept_command(self):
        try:
            sobj = ocs_sal_attribute(self.__mgr, 'acceptCommand_{0:s}'.format(self._name))
            self._cmdid = sobj(self._container)
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self._cmdid = -1

    # +
    # (hidden) method: _ack_command()
    # -
    def _ack_command(self, code=0, msg=''):
        try:
            self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} entry'.format(
                self._entity, self._name, str(self._ackval)))
            sobj = ocs_sal_attribute(self.__mgr, 'ackCommand_{0:s}'.format(self._name))
            self._ackval = sobj(self._cmdid, code, 0, msg)
            self._log.logger.info('{0:s} {1:s} thread _ack_command()={2:s} exit'.format(
                self._entity, self._name, str(self._ackval)))
        except OcsGenericEntityException as e:
            self._log.logger.critical(e.errstr)
            self._ackval = -1

    # +
    # (hidden) method: _change_state_event()
    # -
    def _change_state_event(self):
        msg = '{0:s}EntitySummaryState'.format(self._entity_lc)
        self._log.logger.info("{0:s} {1:s} thread _change_state_event('{2:s}') entry".format(
            self._entity, self._name, msg))
        self._evh.send_event(msg,
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

    # +
    # method: _generic_sequence()
    # -
    def _generic_sequence(self, indict=None):

        # get input
        self._indict = indict

        # check input(s)
        if not isinstance(self._indict, dict) or not self._indict:
            return self._ack_command(SAL__CMD_FAILED, 'Error : No Dicitionary')

        # make sure entity is set to and entity
        if 'entity' not in self._indict or self._indict['entity'] == '':
            return self._ack_command(SAL__CMD_FAILED, 'Error : No Entity')

        else:

            # get command object
            self._cmdr = None
            self._cmde = self._indict['entity'].lower()
            self._log.logger.info('{0:s} {0:s} thread <cmde>> {2:s}'.format(self._entity, self._name, str(self._cmde)))
            if self._cmde in self._indict and self._indict[self._cmde]:
                self._log.logger.info('{0:s} {0:s} thread <<cmde>> {2:s}'.format(self._entity, self._name, str(self._cmde)))
                self._cmdr = self._indict[self._cmde]
                self._log.logger.info('{0:s} {0:s} thread <cmdr> {2:s}'.format(self._entity, self._name, str(self._cmdr)))

            if 'timeout' in self._indict and self._indict['timeout'] != None:
                self._timeout = int(self._indict['timeout'])
            else:
                self._timeout = OCS_GENERIC_COMMAND_TIMEOUT

            self._log.logger.info('{0:s} {0:s} thread <<<cmde>>> {2:s}'.format(self._entity, self._name, str(self._cmde)))
            self._log.logger.info('{0:s} {0:s} thread <<cmdr>> {2:s}'.format(self._entity, self._name, str(self._cmdr)))
            self._log.logger.info('{0:s} {0:s} thread timeout {2:d}'.format(self._entity, self._name, self._timeout))
            self._log.logger.info('{0:s} {0:s} thread invoking {2:s}'.format(self._entity, self._name, self._indict['cmd']))

            # set busy flag
            self._smc.setBusy = True

            # execute generic command
            if self._cmdr:
                if self._indict['cmd'].lower() == 'abort':
                    self._cmdr.abort(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'disable':
                    self._cmdr.disable(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'enable':
                    self._cmdr.enable(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'entercontrol':
                    self._cmdr.entercontrol(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'exitcontrol':
                    self._cmdr.exitcontrol(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'standby':
                    self._cmdr.standby(timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'start':
                    self._startid = self._indict['params'].split('=')[1]
                    self._log.logger.info('{0:s} {0:s} thread startid {2:s}'.format(self._entity, self._name, self._startid))
                    self._cmdr.start(startid=self._startid, timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                elif self._indict['cmd'].lower() == 'stop':
                    self._device = self._indict['params'].split('=')[1]
                    self._log.logger.info('{0:s} {0:s} thread device {2:s}'.format(self._entity, self._name, self._device))
                    self._cmdr.stop(device=self._device, timeout=self._timeout)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

                else:
                    self._ack_command(SAL__CMD_FAILED, 'Error : No Command')

            # unset busy flag
            self._smc.setBusy = False

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
            self._smc.setBusy = False
            return

        # do something
        else:

            # reset state change flag
            self._state_flag = False

            # change state (as appropriate)
            if self._name == 'abort'and current_state != OCS_SUMMARY_STATE_FAULT:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_FAULT)
                self._state_flag = True

            elif self._name == 'disable' and current_state == OCS_SUMMARY_STATE_ENABLED:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_DISABLED)
                self._state_flag = True

            elif self._name == 'enable' and current_state == OCS_SUMMARY_STATE_DISABLED:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_ENABLED)
                self._state_flag = True

            elif self._name == 'enterControl' and (current_state == OCS_SUMMARY_STATE_UNKNOWN or current_state == OCS_SUMMARY_STATE_OFFLINE):
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_STANDBY)
                self._state_flag = True

            elif self._name == 'exitControl' and current_state == OCS_SUMMARY_STATE_STANDBY:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_OFFLINE)
                self._state_flag = True

            elif self._name == 'standby' and current_state == OCS_SUMMARY_STATE_DISABLED:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_STANDBY)
                self._state_flag = True

            elif self._name == 'start' and current_state == OCS_SUMMARY_STATE_STANDBY:
                self._smc.change_state(current_state, OCS_SUMMARY_STATE_DISABLED)
                self._state_flag = True

            # these do not need a state change
            elif self._name == 'setValue':
                self._state_flag = False
                self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

            elif self._name == 'stop':
                self._state_flag = False
                self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

            elif self._name == 'sequence':
                self._state_flag = False
                self._evh.logger.info('{0:s} thread received payload {1:s}'.format(self._name, str(self._container.command)))
                ltsd = ocs_sal_lts237(self._container.command)
                if ltsd['entity'].lower() == 'all':
                    for E in ('Archiver', 'Camera', 'CatchupArchiver', 'ProcessingCluster', 'Tcs'):
                        ltsd['entity'] = E.lower()
                        if ltsd['cmd'].lower() == 'start':
                            #ltsd['params'] = 'startid={0:s}-Normal'.format(E)
                            ltsd['params'] = 'startid=Normal'
                        cmdd = dict(self._objd, **ltsd)
                        self._evh.logger.info('{0:s} thread cmdd {1:s}'.format(self._name, str(cmdd)))
                        self._generic_sequence(cmdd)
                else:
                    cmdd = dict(self._objd, **ltsd)
                    self._evh.logger.info('{0:s} thread cmdd {1:s}'.format(self._name, str(cmdd)))
                    self._generic_sequence(cmdd)

            elif self._name == 'script':
                self._state_flag = False
                self._evh.logger.info('{0:s} thread received payload {1:s}'.format(self._name, str(self._container.location)))
                # import the script
                try:
                    self._log.logger.info('Importing {0:s}'.format(self._container.location))
                    sobj = ocs_sal_import(self._container.location)
                except:
                    sobj = None
                    self._ack_command(SAL__CMD_FAILED, 'Error : No Import')
                # get the script function
                try:
                    self._log.logger.info('Importing {0:s}_main'.format(self._container.location))
                    aobj = ocs_sal_attribute(sobj, '{0:s}_main'.format(self._container.location))
                except:
                    aobj = None
                    self._ack_command(SAL__CMD_FAILED, 'Error : No Attribute')
                else:
                    # do something
                    aobj(self._arc, self._cam, self._cat, self._pro, self._tel)
                    self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

            # generate a state change event
            if self._state_flag:
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
                self._ack_command(SAL__CMD_COMPLETE, 'Done : OK')

        # set state machine to not busy
        self._smc.setBusy = False

    # +
    # (hidden) method: _dump_payload()
    # -
    def _dump_payload(self):
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
        elif self._name == 'sequence':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.command)))
        elif self._name == 'script':
            self._log.logger.info('{0:s} {1:s} thread payload state={2:s}'.format(
                self._entity, self._name, str(self._container.location)))

    # +
    # method: run()
    # -
    def run(self):

        # shutdown_flag is a threading.Event object that indicates whether the thread should be terminated
        self.shutdown_flag = threading.Event()

        # set up logging
        self._log = OcsLogger(self._entity, self._name)
        self._log.logger.info('{0:s} {1:s} thread starting up'.format(self._entity, self._name))

        # connection to middleware
        self._get_sal_connection()
        self._get_mgr_connection()
        self._setup_processor()
        self._get_container()

        # set up object dictionary
        self._objd = {}
        if self._name == 'sequence':
            self._objd['camera'] = self._cam
            self._objd['tcs'] = self._tel
            self._objd['archiver'] = self._arc
            self._objd['catchuparchiver'] = self._cat
            self._objd['processingcluster'] = self._pro

        # loop until signal arrives from main thread
        self._log.logger.info('{0:s} {1:s} thread entering loop'.format(self._entity, self._name))
        while not self.shutdown_flag.is_set():

            # accept a command
            self._accept_command()

            # process the command
            if self._cmdid > 0:
                self._log.logger.info('{0:s} {1:s} thread command identifier {2:d}'.format(self._entity, self._name, self._cmdid))

                # dump payload
                self._dump_payload()

                # do something
                self._process_command()

            # this sleep means it's really polling?!
            time.sleep(1)

        # exit message
        self.__mgr.salShutdown()
        self._log.logger.info('{0:s} {1:s} thread shutting down'.format(self._entity, self._name))


# +
# main()
# -
if __name__ == "__main__":

    # register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    # create logger and state machine
    event_processor = OcsEvents(False)
    state_machine = OcsStates()

    # create commandable entities
    camera = OcsCameraEntity('CCS', 'Camera', False)
    tcs = OcsGenericEntity('TCS', 'Tcs', False)
    archiver = OcsGenericEntity('DMCS', 'Archiver', False)
    catchuparchiver = OcsGenericEntity('DMCS', 'CatchupArchiver', False)
    processingcluster = OcsGenericEntity('DMCS', 'ProcessingCluster', False)

    # set up state machine
    if state_machine:
        state_machine.change_state(OCS_SUMMARY_STATE_UNKNOWN, OCS_SUMMARY_STATE_OFFLINE)

    # start main and worker threads
    threads = []
    try:
        # create threads for each generic command
        for T in ['abort', 'disable', 'enable', 'enterControl', 'exitControl', 'standby', 'start', 'stop']:
            t = Worker(T, 'Sequencer', event_processor, state_machine, None, None, None, None, None)
            threads.append(t)
            t.start()

        # create threads for each behavioural command
        for T in ['sequence', 'script']:
            t = Worker(T, 'Sequencer', event_processor, state_machine, camera, tcs, archiver, catchuparchiver, processingcluster)
            threads.append(t)
            t.start()

        # main thread: keep running to collect signals and publish heartbeat
        mgr = SAL_sequencer()
        mgr.salTelemetryPub("sequencer_SequencerHeartbeat")
        hbData = sequencer_SequencerHeartbeatC()
        hbData.Name = "OcsSequencer"
        hbData.Identifier = float(ocs_id(False))
        icount = 1
        while True:
            if (icount % OCS_SEQUENCER_COMMAND_TIMEOUT == 0):
                hbData.Timestamp = ocs_id(True)
                retval = mgr.putSample_SequencerHeartbeat(hbData)
                icount = 1
            else:
                icount += 1
            time.sleep(1)

    except ServiceExit:
        # set flag in threads
        for t in threads:
            t.shutdown_flag.set()
        # wait for flags to exit
        for t in threads:
            t.join()
