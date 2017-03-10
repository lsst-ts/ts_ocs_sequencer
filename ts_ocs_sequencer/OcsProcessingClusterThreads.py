#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from __future__ import print_function
import argparse
import sys
import threading
import time
from ocs_common import *
from OcsLogger import *
from OcsEvents import *
from OcsStates import *
from SALPY_processingcluster import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "1 February 2017"
__doc__ = """Commander for the OCS ProcessingCluster using Python Threading"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsProcessingClusterThreads.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: thread_code()
# -
def thread_code(entity='', evp=None, smachine=None):

    # declare some variables and initialize them
    thread_name = threading.currentThread().getName()
    thread_id = threading.currentThread()
    thread_entity = entity

    # did we get input objects?
    if evp:
        evp.logger.info('{0:s} thread received event handler at address {1:s}'.format(thread_name, hex(id(evp))))
    if smachine:
        smachine.logger.info('{0:s} thread received smachine entity at address {1:s}'.format(thread_name, hex(id(smachine))))

    # get logger
    evlog = OcsLogger('ProcessingCluster', thread_name)
    evlog.logger.info('{0:s} thread starting up'.format(thread_name))

    # get and reset dictionaries
    state_dict = ocsEntitySummaryState
    cmd_dict = ocsEntitySummaryStateCommands
    cfg_dict = ocsEntitySummaryStateConfigurations
    cfg_dict[OCS_SUMMARY_STATE_STANDBY] = ['{0:s}-Normal'.format(entity.lower())]
    evlog.logger.info('{0:s} thread configs'.format(str(cfg_dict)))

    # connect to SAL
    mgr = SAL_processingcluster()
    if not mgr:
        evlog.logger.error('{0:s} thread failed to connect to SAL'.format(thread_name))
        return
    evlog.logger.info('{0:s} thread connected to SAL'.format(thread_name))

    # get processor
    if thread_name == 'abort':
        mgr.salProcessor('processingcluster_command_abort')
    elif thread_name == 'disable':
        mgr.salProcessor('processingcluster_command_disable')
    elif thread_name == 'enable':
        mgr.salProcessor('processingcluster_command_enable')
    elif thread_name == 'enterControl':
        mgr.salProcessor('processingcluster_command_enterControl')
    elif thread_name == 'exitControl':
        mgr.salProcessor('processingcluster_command_exitControl')
    elif thread_name == 'setValue':
       #mgr.salProcessor('processingcluster_command_setValue')
        pass
    elif thread_name == 'standby':
        mgr.salProcessor('processingcluster_command_standby')
    elif thread_name == 'start':
        mgr.salProcessor('processingcluster_command_start')
    elif thread_name == 'stop':
        mgr.salProcessor('processingcluster_command_stop')
    else:
        evlog.logger.error('{0:s} thread processor error'.format(thread_name))
        return
    evlog.logger.info('{0:s} thread processor created'.format(thread_name))

    # get payload container
    if thread_name == 'abort':
        data = processingcluster_command_abortC()
       #smachine.setFlag(OCS_SEQUENCER_ABORT_OFFSET)
    elif thread_name == 'disable':
        data = processingcluster_command_disableC()
       #smachine.setFlag(OCS_SEQUENCER_DISABLE_OFFSET)
    elif thread_name == 'enable':
        data = processingcluster_command_enableC()
       #smachine.setFlag(OCS_SEQUENCER_ENABLE_OFFSET)
    elif thread_name == 'enterControl':
        data = processingcluster_command_enterControlC()
       #smachine.setFlag(OCS_SEQUENCER_ENTERCONTROL_OFFSET)
    elif thread_name == 'exitControl':
        data = processingcluster_command_exitControlC()
       #smachine.setFlag(OCS_SEQUENCER_EXITCONTROL_OFFSET)
    elif thread_name == 'setvalue':
        data = processingcluster_command_setvalueC()
       #smachine.setFlag(OCS_SEQUENCER_SETVALUE_OFFSET)
    elif thread_name == 'standby':
        data = processingcluster_command_standbyC()
       #smachine.setFlag(OCS_SEQUENCER_STANDBY_OFFSET)
    elif thread_name == 'start':
        data = processingcluster_command_startC()
       #smachine.setFlag(OCS_SEQUENCER_START_OFFSET)
    elif thread_name == 'stop':
        data = processingcluster_command_stopC()
       #smachine.setFlag(OCS_SEQUENCER_STOP_OFFSET)
    else:
        evlog.logger.error('{0:s} thread payload container error'.format(thread_name))
        return

    # info
    evlog.logger.info('{0:s} thread payload container created'.format(thread_name))
    evlog.logger.info('{0:s} thread {1:s} flags={2:d}'.format(thread_entity, thread_name, int(smachine._flags)))
    evlog.logger.info('{0:s} thread {1:s} ready'.format(thread_entity, thread_name))

    # loop forever
    while True:

        # accept command
        if thread_name == 'abort':
            cmdId = mgr.acceptCommand_abort(data)
        elif thread_name == 'disable':
            cmdId = mgr.acceptCommand_disable(data)
        elif thread_name == 'enable':
            cmdId = mgr.acceptCommand_enable(data)
        elif thread_name == 'enterControl':
            cmdId = mgr.acceptCommand_enterControl(data)
        elif thread_name == 'exitControl':
            cmdId = mgr.acceptCommand_exitControl(data)
        elif thread_name == 'standby':
            cmdId = mgr.acceptCommand_standby(data)
        elif thread_name == 'start':
            cmdId = mgr.acceptCommand_start(data)
        elif thread_name == 'stop':
            cmdId = mgr.acceptCommand_stop(data)

        # process command
        if cmdId > 0:
            evlog.logger.info('{0:s} thread command identifier {1:d}'.format(thread_name, cmdId))

            if thread_name == 'abort':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                if smachine:
                    smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_FAULT)
                    if evp:
                        thread_ocsid = ocs_id(False)
                        nsta = state_dict.get(smachine._current_state, '')
                        osta = state_dict.get(smachine._previous_state, '')
                        cmds = cmd_dict.get(smachine._current_state, [])
                        cfgs = cfg_dict.get(smachine._current_state, [])
                        evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                            Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                            Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'disable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_disable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_disable(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_DISABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_disable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'enable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_enable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_enable(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_ENABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_enable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'enterControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_STANDBY)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'exitControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_OFFLINE)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'standby':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_standby(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_standby(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_STANDBY)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_standby(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'start':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.configuration)))
                smachine.setBusy = True
                retval = mgr.ackCommand_start(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = cmd_dict.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(state_dict.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_start(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_DISABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = state_dict.get(smachine._current_state, '')
                            osta = state_dict.get(smachine._previous_state, '')
                            cmds = cmd_dict.get(smachine._current_state, [])
                            cfgs = cfg_dict.get(smachine._current_state, [])
                            evp.sendEvent('processingclusterEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_start(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'stop':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_stop(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_stop(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            evlog.logger.info('{0:s} thread command return value {1:d}'.format(thread_name, retval))

        # I think this sleep means it's really polling?!
        time.sleep(1)

    evlog.logger.info('{0:s} thread {1:s} shutting down'.format(thread_entity, thread_name))
    mgr.salShutdown()
    return True

# +
# main()
# -
if __name__ == "__main__":

    # created shared entities
    evp = OcsEvents(False)
    smachine = OcsStates()

    # set up state machine
    if smachine:
        smachine.change_state(OCS_SUMMARY_STATE_UNKNOWN, OCS_SUMMARY_STATE_OFFLINE)
        smachine._shutdown = False

    # create threads for each command:
    threads = []
    for T in [ 'abort', 'disable', 'enable', 'enterControl', 'exitControl', 'standby', 'start', 'stop']:
        t = threading.Thread(name=T, target=thread_code, args=('ProcessingCluster', evp, smachine))
        threads.append(t)
        t.start()
