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
from SALPY_ocs import *

from OcsCameraEntity import *

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "1 February 2017"
__doc__ = """Commander for the OCS Sequencer"""
__email__ = "pdaly@lsst.org"
__file__ = "sequencer_ocs.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: parse_command()
# -

def parse_command(incmd=''):

    # default dictionary
    retdic  = { 'cmd': None, 'entity': None, 'params': None, 'timeout': None }

    # check input parameters
    if not isinstance(incmd, str) or incmd=='':
        pass

    # parse input command
    else:
        clist = [ 'abort', 'disable', 'enable', 'entercontrol', 'exitcontrol', 'setvalue', 'standby', 'start', 'stop' ]
        alist = [ 'device=', 'parameter=', 'startid=', 'value=' ]
        words = incmd.split()

        # loop around words
        for E in words:
            El = E.lower()
            if El in clist:
                retdic['cmd'] = El
            if El.find('entity=') >= 0:
                retdic['entity'] = El.split('=')[1]
            if El.find('timeout=') >= 0:
                try:
                    value = int(El.split('=')[1])
                except ValueError:
                    value = None
                retdic['timeout'] = value
            for A in alist:
                if El.find(A) >= 0:
                    if retdic['params'] == None:
                        retdic['params'] = E
                    else:
                        retdic['params'] = '{0:s} {1:s}'.format(retdic['params'], E)
    # return dictionary
    return retdic

# +
# function: thread_code()
# -
def thread_code(entity='', evp=None, camera=None):

    # declare some variables and initialize them
    thread_name = threading.currentThread().getName();
    thread_id = threading.currentThread()
    thread_state = 'OFFLINE-AVAILABLE'
    thread_entity = entity

    # did we get input objects?
    if evp:
        evp.logger.info('{0:s} thread received event handler at address {1:s}'.format(thread_name, hex(id(camera))))
    if camera:
        camera.logger.info('{0:s} thread received camera entity at address {1:s}'.format(thread_name, hex(id(camera))))

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
    elif thread_name == 'disable':
        data = ocs_command_disableC()
    elif thread_name == 'enable':
        data = ocs_command_enableC()
    elif thread_name == 'enterControl':
        data = ocs_command_enterControlC()
    elif thread_name == 'exitControl':
        data = ocs_command_exitControlC()
    elif thread_name == 'sequence':
        data = ocs_command_sequenceC()
    elif thread_name == 'script':
        data = ocs_command_scriptC()
    elif thread_name == 'standby':
        data = ocs_command_standbyC()
    elif thread_name == 'start':
        data = ocs_command_startC()
    elif thread_name == 'stop':
        data = ocs_command_stopC()
    else:
        evlog.logger.error('{0:s} thread payload container error'.format(thread_name))
        return
    evlog.logger.info('{0:s} thread payload container created'.format(thread_name))

    # loop forever
    evlog.logger.info('{0:s} thread {1:s} ready'.format(thread_entity, thread_name))
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

            if thread_name == 'abort':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'FAULT'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='STANDBY | DISABLED | ENABLED',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_abort(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'disable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_disable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'DISABLED'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='ENABLED',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='enable standby', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_disable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'enable':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_enable(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'ENABLED'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='DISABLED',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='disable', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_enable(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'enterControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'STANDBY'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='OFFLINE-AVAILABLE',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='start', ConfigurationsAvailable='Normal', priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_enterControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'exitControl':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'OFFLINE-AVAILABLE'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='STANDBY',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='enterControl', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_exitControl(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'sequence':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.command)))
                cmddict = parse_command(data.command)
                evlog.logger.info('{0:s} thread cmddict {1:s}'.format(thread_name, str(cmddict)))
                if camera:
                    if cmddict:
                        if cmddict['entity']=='camera':
                            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                            if 'timeout' in cmddict and cmddict['timeout']!=None:
                                timeout = cmddict['timeout']
                            else:
                                timeout = OCS_CAMERA_COMMAND_TIMEOUT
                            evlog.logger.info('{0:s} thread timeout {1:d}'.format(thread_name, timeout))
                            evlog.logger.info('{0:s} thread invoking {1:s}'.format(thread_name, cmddict['cmd']))
                            if cmddict['cmd'] == 'abort':
                                camera.abort(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'disable':
                                camera.disable(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'enable':
                                camera.enable(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'entercontrol':
                                camera.entercontrol(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'exitcontrol':
                                camera.exitcontrol(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'standby':
                                camera.standby(timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'start':
                                startid = cmddict['params'].split('=')[1]
                                evlog.logger.info('{0:s} thread startid {1:s}'.format(thread_name, startid))
                                camera.start(startid=startid, timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            elif cmddict['cmd'] == 'stop':
                                device = cmddict['params'].split('=')[1]
                                evlog.logger.info('{0:s} thread device {1:s}'.format(thread_name, device))
                                camera.stop(device=device, timeout=timeout)
        			retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
                            else:
                                retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Command");
                        else:
                            retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Entry");
                    else:
                        retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Dictionary");
                else:
                    retval = mgr.ackCommand_sequence(cmdId, SAL__CMD_FAILED, 0, "Error : No Camera");

            elif thread_name == 'script':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.location)))
                retval = mgr.ackCommand_script(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_script(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'standby':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_standby(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'STANDBY'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_name, NewState=thread_state, OldState='DISABLED',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='exitControl start', ConfigurationsAvailable='Normal', priority=SAL__EVENT_INFO)
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_standby(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'start':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.configuration)))
                retval = mgr.ackCommand_start(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'DISABLED'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='OFFLINE-AVAILABLE',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='enable standby', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                time.sleep(1) # really want to do something here
                retval = mgr.ackCommand_start(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");

            elif thread_name == 'stop':
                evlog.logger.info('{0:s} thread received payload {1:s}'.format(thread_name, str(data.state)))
                retval = mgr.ackCommand_stop(cmdId, SAL__CMD_INPROGRESS, 0, "Ack : OK");
                thread_state = 'ENABLED'
                if evp:
                    thread_ocsid = ocs_id(False)
                    evp.sendEvent('ocsEntitySummaryState', Name=thread_entity, NewState=thread_state, OldState='ENABLED',
                        Identifier=thread_ocsid, Timestamp=ocs_mjd_to_iso(thread_ocsid), Executing=thread_name,
                        Address=id(thread_id), CommandsAvailable='sequence script', ConfigurationsAvailable='', priority=SAL__EVENT_INFO)
                retval = mgr.ackCommand_stop(cmdId, SAL__CMD_COMPLETE, 0, "Done : OK");
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

    # create threads for each command:
    threads = []
    for T in [ 'abort', 'disable', 'enable', 'enterControl', 'exitControl', 'sequence', 'script', 'standby', 'start', 'stop']:
        t = threading.Thread(name=T, target=thread_code, args=('Sequencer', evp, camera,))
        threads.append(t)
        t.start()
