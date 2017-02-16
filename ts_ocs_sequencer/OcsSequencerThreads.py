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
from OcsStates import *
from SALPY_ocs import *

from OcsCameraEntity import *

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "1 February 2017"
__doc__ = """Commander for the OCS Sequencer using Python Threading"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsSequencerThreads.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: lts237()
# -
def lts237(incmd=''):

    # default dictionary
    retdic  = {
        'cmd': None,
        'entity': None,
        'params': None,
        'timeout': None,
        }

    # check input parameters
    if not isinstance(incmd, str) or incmd=='':
        pass

    # parse input command
    else:
        clist = [ 'abort', 'disable', 'enable', 'entercontrol', 'exitcontrol', 'setvalue', 'standby', 'start', 'stop' ]
        tlist = [ 'timeout=' ]
        alist = [ 'device=', 'parameter=', 'startid=', 'value=' ]
        words = incmd.split()

        # loop around words
        for E in words:
            El = E.lower()

            # get the command
            if El in clist:
                retdic['cmd'] = El

            # get the entity
            if El.find('entity=') >= 0:
                retdic['entity'] = El.split('=')[1]

            # get any timeout
            for T in tlist:
                if El.find(T) >= 0:
                    try:
                        value = int(El.split('=')[1])
                    except ValueError:
                        value = None
                    retdic['timeout'] = value

            # get other arguments
            for A in alist:
                if El.find(A) >= 0:
                    if retdic['params'] == None:
                        retdic['params'] = E
                    else:
                        retdic['params'] = '{0:s} {1:s}'.format(retdic['params'], E)

    # return dictionary
    return retdic

# +
# function: camera_sequence()
# -
def camera_sequence(indict={}):

    # check input(s)
    if not indict:
        return -1

    # get some objects
    mgr = indict['mgr']
    camera = indict['camera']
    smachine = indict['smachine']
    cmdId = indict['cmdId']
    name = indict['name']
    evlog = indict['evlog']

    # make sure entity is set to camera
    if indict['entity'].lower() != 'camera':
        return mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Entity")

    else:
        smachine.setBusy = True
        retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
        if 'timeout' in indict and indict['timeout']!=None:
            timeout = indict['timeout']
        else:
            timeout = OCS_CAMERA_COMMAND_TIMEOUT

        evlog.logger.info('{0:s} thread timeout {1:d}'.format(name, timeout))
        evlog.logger.info('{0:s} thread invoking {1:s}'.format(name, indict['cmd']))

        if indict['cmd'].lower() == 'abort':
            camera.abort(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'disable':
            camera.disable(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'enable':
            camera.enable(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'entercontrol':
            camera.entercontrol(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'exitcontrol':
            camera.exitcontrol(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'standby':
            camera.standby(timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'start':
            startid = indict['params'].split('=')[1]
            evlog.logger.info('{0:s} thread startid {1:s}'.format(name, startid))
            camera.start(startid=startid, timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        elif indict['cmd'].lower() == 'stop':
            device = indict['params'].split('=')[1]
            evlog.logger.info('{0:s} thread device {1:s}'.format(name, device))
            camera.stop(device=device, timeout=timeout)
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

        else:
            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Command")

        smachine.setBusy = False
        return retval


# +
# function: thread_code()
# -
def thread_code(entity='', evp=None, camera=None, smachine=None):

    # declare some variables and initialize them
    thread_name = threading.currentThread().getName()
    thread_id = threading.currentThread()
    thread_entity = entity

    # did we get input objects?
    if evp:
        evp.logger.info('{0:s} thread received event handler at address {1:s}'.format(thread_name, hex(id(evp))))
    if camera:
        camera.logger.info('{0:s} thread received camera entity at address {1:s}'.format(thread_name, hex(id(camera))))
    if smachine:
        smachine.logger.info('{0:s} thread received smachine entity at address {1:s}'.format(thread_name, hex(id(smachine))))

    # get logger
    evlog = OcsLogger('Sequencer', thread_name)
    evlog.logger.info('{0:s} thread starting up'.format(thread_name))

    # connect to SAL
    mgr = SAL_ocs()
    if not mgr:
        evlog.logger.error('{0:s} thread failed to connect to SAL'.format(thread_name))
        return
    evlog.logger.info('{0:s} thread connected to SAL'.format(thread_name))

    # get processor
    if thread_name == 'abort':
        mgr.salProcessor('ocs_command_abort')
    elif thread_name == 'disable':
        mgr.salProcessor('ocs_command_disable')
    elif thread_name == 'enable':
        mgr.salProcessor('ocs_command_enable')
    elif thread_name == 'enterControl':
        mgr.salProcessor('ocs_command_enterControl')
    elif thread_name == 'exitControl':
        mgr.salProcessor('ocs_command_exitControl')
    elif thread_name == 'sequence':
        mgr.salProcessor('ocs_command_sequence')
    elif thread_name == 'script':
        mgr.salProcessor('ocs_command_script')
    elif thread_name == 'setValue':
        #mgr.salProcessor('ocs_command_setValue')
        pass
    elif thread_name == 'shutdown':
        #mgr.salProcessor('ocs_command_shutdown')
        pass
    elif thread_name == 'standby':
        mgr.salProcessor('ocs_command_standby')
    elif thread_name == 'start':
        mgr.salProcessor('ocs_command_start')
    elif thread_name == 'stop':
        mgr.salProcessor('ocs_command_stop')
    else:
        evlog.logger.error('{0:s} thread processor error'.format(thread_name))
        return
    evlog.logger.info('{0:s} thread processor created'.format(thread_name))

    # get payload container
    if thread_name == 'abort':
        data = ocs_command_abortC()
        smachine.setFlag(OCS_SEQUENCER_ABORT_OFFSET)
    elif thread_name == 'disable':
        data = ocs_command_disableC()
        smachine.setFlag(OCS_SEQUENCER_DISABLE_OFFSET)
    elif thread_name == 'enable':
        data = ocs_command_enableC()
        smachine.setFlag(OCS_SEQUENCER_ENABLE_OFFSET)
    elif thread_name == 'enterControl':
        data = ocs_command_enterControlC()
        smachine.setFlag(OCS_SEQUENCER_ENTERCONTROL_OFFSET)
    elif thread_name == 'exitControl':
        data = ocs_command_exitControlC()
        smachine.setFlag(OCS_SEQUENCER_EXITCONTROL_OFFSET)
    elif thread_name == 'sequence':
        data = ocs_command_sequenceC()
        smachine.setFlag(OCS_SEQUENCER_SEQUENCE_OFFSET)
    elif thread_name == 'script':
        data = ocs_command_scriptC()
        smachine.setFlag(OCS_SEQUENCER_SCRIPT_OFFSET)
    elif thread_name == 'setvalue':
        data = ocs_command_setvalueC()
        smachine.setFlag(OCS_SEQUENCER_SETVALUE_OFFSET)
    elif thread_name == 'standby':
        data = ocs_command_standbyC()
        smachine.setFlag(OCS_SEQUENCER_STANDBY_OFFSET)
    elif thread_name == 'start':
        data = ocs_command_startC()
        smachine.setFlag(OCS_SEQUENCER_START_OFFSET)
    elif thread_name == 'stop':
        data = ocs_command_stopC()
        smachine.setFlag(OCS_SEQUENCER_STOP_OFFSET)
    elif thread_name == 'shutdown':
        data = ocs_command_shutdownC()
        smachine.setFlag(OCS_SEQUENCER_SHUTDOWN_OFFSET)
    else:
        evlog.logger.error('{0:s} thread payload container error'.format(thread_name))
        return

    # info
    evlog.logger.info('{0:s} thread payload container created'.format(thread_name))
    evlog.logger.info('{0:s} thread {1:s} flags={2:d}'.format(thread_entity, thread_name, int(smachine._flags)))
    evlog.logger.info('{0:s} thread {1:s} shutdown={2:s}'.format(thread_entity, thread_name, str(smachine._shutdown)))
    evlog.logger.info('{0:s} thread {1:s} ready'.format(thread_entity, thread_name))

    # set up object dictionary
    objd = {
         'camera': camera,
         'evlog': evlog,
         'mgr': mgr,
         'name': thread_name,
         'smachine': smachine
         }

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
        elif thread_name == 'sequence':
            cmdId = mgr.acceptCommand_sequence(data)
        elif thread_name == 'script':
            cmdId = mgr.acceptCommand_script(data)
        elif thread_name == 'standby':
            cmdId = mgr.acceptCommand_standby(data)
        elif thread_name == 'start':
            cmdId = mgr.acceptCommand_start(data)
        elif thread_name == 'stop':
            cmdId = mgr.acceptCommand_stop(data)

        # process command
        if cmdId > 0:
            evlog.logger.info('{0:s} thread command identifier {1:d}'.format(thread_name, cmdId))
            objd['cmdId'] = cmdId

            if thread_name == 'abort':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                if smachine:
                    smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_FAULT)
                    if evp:
                        thread_ocsid = ocs_id(False)
                        nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                        osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                        cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                        cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                        evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                            Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                            Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'disable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_disable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_disable(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_DISABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_disable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'enable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_enable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_enable(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_ENABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_enable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'enterControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_STANDBY)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'exitControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_OFFLINE)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'sequence':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.command)))
                ltsd = lts237(data.command)
                cmdd = dict(objd, **ltsd)
                #cmdd = {k: v for d in [ltsd, objd] for k, v in ltsd.items()}
                evlog.logger.info('{0:s} thread cmdd {1:s}'.format(thread_name, str(cmdd)))
                retval = camera_sequence(cmdd)

            elif thread_name == 'script':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.location)))
                retval = mgr.ackCommand_script(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_script(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")

            elif thread_name == 'standby':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                smachine.setBusy = True
                retval = mgr.ackCommand_standby(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_standby(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_STANDBY)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
                                Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                                Address=id(thread_id), CommandsAvailable=str(cmds), ConfigurationsAvailable=str(cfgs), priority=SAL__EVENT_INFO)
                    retval = mgr.ackCommand_standby(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK")
                smachine.setBusy = False

            elif thread_name == 'start':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.configuration)))
                smachine.setBusy = True
                retval = mgr.ackCommand_start(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK")
                current_cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                if thread_name.lower() not in current_cmds:
                    msg = 'Error : Command disallowed in {0:s} state'.format(ocsEntitySummaryState.get(smachine._current_state, ''))
                    retval = mgr.ackCommand_start(cmdId, SAL__CMD_FAILED, 0, msg)
                else:
                    if smachine:
                        smachine.change_state(smachine._current_state, OCS_SUMMARY_STATE_DISABLED)
                        if evp:
                            thread_ocsid = ocs_id(False)
                            nsta = ocsEntitySummaryState.get(smachine._current_state, '')
                            osta = ocsEntitySummaryState.get(smachine._previous_state, '')
                            cmds = ocsEntitySummaryStateCommands.get(smachine._current_state, [])
                            cfgs = ocsEntitySummaryStateConfigurations.get(smachine._current_state, [])
                            evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, CurrentState=str(nsta), PreviousState=str(osta),
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
    camera = OcsCameraEntity('CCS', 'Camera', False)
    smachine = OcsStates()

    # set up state machine
    if smachine:
        smachine.change_state(OCS_SUMMARY_STATE_UNKNOWN, OCS_SUMMARY_STATE_OFFLINE)
        smachine._shutdown = False

    # create threads for each command:
    threads = []
    for T in [ 'abort', 'disable', 'enable', 'enterControl', 'exitControl', 'sequence', 'script', 'standby', 'start', 'stop']:
        t = threading.Thread(name=T, target=thread_code, args=('Sequencer', evp, camera, smachine))
        threads.append(t)
        t.start()
