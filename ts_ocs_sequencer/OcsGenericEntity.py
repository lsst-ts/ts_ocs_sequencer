#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from ocs_common import *
from ocs_sal import *
from OcsEvents import *
from OcsExceptions import *
from OcsLogger import *
import random
import time


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Generic entity class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsGenericEntity.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsGenericEntity()
# -
class OcsGenericEntity(object):

    # +
    # method: __init__
    # -
    def __init__(self, system='', entity='', simulate=True):
        """
            :param system: name of system
            :param entity: name of entity
            :param simulate: if True, use simulation
            :return: None or object representing the entity
        """

        # get arguments(s)
        self._system = system
        self._system_lc = self._system.lower()
        self._entity = entity
        self._entity_lc = self._entity.lower()
        self._simulate = simulate

        # check system
        self._system = ocsGenericEntitySystemDictionary.get(self._system_lc, '')
        if self._system == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSYS, "{0:s}".format(system))

        # check entity
        self._entity = ''.join(xi for xi in ocsGenericEntityEntityDictionary.get(
            self._system, []) if xi.lower() == self._entity_lc)
        if self._entity == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOENT, "{0:s}".format(entity))

        # check simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # set up logging
        self.logger = OcsLogger(self._system, self._entity).logger
        self.logger.debug("Starting {0:s} {1:s} commandable entity".format(self._system, self._entity))

        # set up event publication
        self._ocsid = ocs_id(False)
        self._instance_evh = OcsEvents(False)
        self._instance_name = '{0:1}-{1:s}-{2:.17f}'.format(self._system, self._entity, float(self._ocsid))
        if self._instance_evh:
            self._instance_evh.sendEvent('ocsEntityStartup', Name=self._instance_name,
                Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid), 
                Address=id(self), priority=SAL__EVENT_INFO)

        # declare some variables and initialize them
        self.logger.debug("Initializing variables")
        self.__sal = None
        self.__mgr = None
        self.__mgr = None

        # container(s)
        self.__abortC = None
        self.__disableC = None
        self.__enableC = None
        self.__entercontrolC = None
        self.__exitcontrolC = None
        self.__setvalueC = None
        self.__standbyC = None
        self.__startC = None
        self.__stopC = None

        # command id(s)
        self.__abort_id = None
        self.__disable_id = None
        self.__enable_id = None
        self.__entercontrol_id = None
        self.__exitcontrol_id = None
        self.__setvalue_id = None
        self.__standby_id = None
        self.__start_id = None
        self.__stop_id = None

        # return value(s)
        self.__abort_retval = None
        self.__disable_retval = None
        self.__enable_retval = None
        self.__entercontrol_retval = None
        self.__exitcontrol_retval = None
        self.__setvalue_retval = None
        self.__standby_retval = None
        self.__start_retval = None
        self.__stop_retval = None

        # other variable(s)
        self._aname = None
        self._cname = None
        self._device = None
        self._ename = None
        self._mname = None
        self._ocsid = None
        self._parameter = None
        self._startid = None
        self._timeout = None
        self._value = None

        # import the SAL component (cf. from SALPY_camera import *)
        self._mname = 'SALPY_{0:s}'.format(self._entity_lc)
        self.logger.debug("Importing {0:s}".format(self._mname))
        self.__sal = ocs_sal_import(self._mname)
        if self.__sal:
            self.logger.debug("Imported {0:s} ok".format(self._mname))

        # get mgr object (cf. mgr = SAL_camera())
        self._aname = 'SAL_{0:s}'.format(self._entity_lc)
        self.logger.debug("Getting attribute {0:s}".format(self._aname))
        mgr = ocs_sal_attribute(self.__sal, self._aname)
        if mgr:
            self.__mgr = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(self._aname))

        # get data structure(s) (cf. data = camera_command_abortC())
        self.__abortC = self._get_sal_cmdC('abort')
        self.__disableC = self._get_sal_cmdC('disable')
        self.__enableC = self._get_sal_cmdC('enable')
        self.__entercontrolC = self._get_sal_cmdC('enterControl')
        self.__exitcontrolC = self._get_sal_cmdC('exitControl')
        # ToBeEnabled: self.__setvalueC = self._get_sal_cmdC('setValue')
        self.__standbyC = self._get_sal_cmdC('standby')
        self.__startC = self._get_sal_cmdC('start')
        self.__stopC = self._get_sal_cmdC('stop')

        # define generic command(s) help
        self.generic_help = (
            'abort        system={0:s} entity={1:s}'.format(self._system, self._entity),
            'disable      system={0:s} entity={1:s}'.format(self._system, self._entity),
            'enable       system={0:s} entity={1:s}'.format(self._system, self._entity),
            'entercontrol system={0:s} entity={1:s}'.format(self._system, self._entity),
            'exitcontrol  system={0:s} entity={1:s}'.format(self._system, self._entity),
            'setvalue     system={0:s} entity={1:s} parameter=<string> value=<string>'.format(self._system, self._entity),
            'standby      system={0:s} entity={1:s}'.format(self._system, self._entity),
            'start        system={0:s} entity={1:s} startid=<string>'.format(self._system, self._entity),
            'stop         system={0:s} entity={1:s} device=<string>'.format(self._system, self._entity)
            )

        # set up a default commander (cf. mgr.salCommand("camera_command_abort"))
        self._cname = '{0:s}_command_abort'.format(self._entity_lc)
        if self.__mgr:
            self.__mgr.salCommand(self._cname)

        # log message on exit
        self.logger.debug("Started {0:s} {1:s} commandable entity ok".format(self._system, self._entity))

    # +
    # method: __del__()
    # -
    def __del__(self):
        if self._instance_evh:
            self._ocsid = ocs_id(False)
            self._instance_evh.sendEvent('ocsEntityShutdown', Name=self._instance_name,
                Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid), 
                Address=id(self), priority=SAL__EVENT_INFO)

    # +
    # (hidden) method: _get_sal_cmdC()
    # -
    def _get_sal_cmdC(self, command=''):
        sname = '{0:s}_command_{1:s}C'.format(self._entity_lc,command)
        self.logger.debug("Getting attribute {0:s}".format(sname))
        so = ocs_sal_attribute(self.__sal, sname)
        if so:
            self.logger.debug("Got attribute {0:s} ok".format(sname))
            return so()
        else:
            return None

    # +
    # (hidden) method: _get_cmd_status()
    # -
    def _get_cmd_status(self, command='', seqnum=-1, retval=-1):
        if retval == SAL__CMD_ACK:
            self._status='{0:s} ({1:d}) acknowledged'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_INPROGRESS:
            self._status='{0:s} ({1:d}) in progress'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_STALLED:
            self._status='{0:s} ({1:d}) stalled'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_COMPLETE:
            self._status='{0:s} ({1:d}) complete'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_NOPERM:
            self._status='{0:s} ({1:d}) no permission'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_NOACK:
            self._status='{0:s} ({1:d}) no acknowledgement'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_FAILED:
            self._status='{0:s} ({1:d}) failed'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_ABORTED:
            self._status='{0:s} ({1:d}) aborted'.format(command, seqnum)
            self.logger.debug(self._status)
        elif retval == SAL__CMD_TIMEOUT:
            self._status='{0:s} ({1:d}) timed out'.format(command, seqnum)
            self.logger.debug(self._status)
        else:
            self._status='{0:s} ({1:d}) unknown error'.format(command, seqnum)
            self.logger.critical(self._status)

        if self._instance_evh:
            self._ocsid = ocs_id(False)
            self._instance_evh.sendEvent('ocsCommandStatus', CommandSource=self._instance_name,
                SequenceNumber=long(seqnum), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                CommandSent=command, Status=self._status, StatusValue=long(retval), priority=SAL__EVENT_INFO)

    # +
    # method: abort()
    # -
    def abort(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("abort() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("abort(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__abortC:
                self._cname = '{0:s}_command_abort'.format(self._entity_lc)
                self._ename = '{0:s}_command_abort timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_abort"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_abortC(); data.state = 'ok')
                self.__abortC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_abort(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__abort_id = self.__mgr.issueCommand_abort(self.__abortC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__abort_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__abort_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_abort(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__abort_retval = self.__mgr.waitForCompletion_abort(self.__abort_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__abort_retval))
                    self._get_cmd_status(self._ename, self.__abort_id, self.__abort_retval)
        self.logger.debug("abort() exit")

    # +
    # method: disable()
    # -
    def disable(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("disable() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("disable(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__disableC:
                self._cname = '{0:s}_command_disable'.format(self._entity_lc)
                self._ename = '{0:s}_command_disable timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_disable"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_disableC(); data.state = 'ok')
                self.__disableC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_disable(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__disable_id = self.__mgr.issueCommand_disable(self.__disableC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__disable_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__disable_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_disable(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__disable_retval = self.__mgr.waitForCompletion_disable(self.__disable_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__disable_retval))
                    self._get_cmd_status(self._ename, self.__disable_id, self.__disable_retval)
        self.logger.debug("disable() exit")

    # +
    # method: enable()
    # -
    def enable(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("enable() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("enable(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__enableC:
                self._cname = '{0:s}_command_enable'.format(self._entity_lc)
                self._ename = '{0:s}_command_enable timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_enable"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_enableC(); data.state = 'ok')
                self.__enableC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_enable(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__enable_id = self.__mgr.issueCommand_enable(self.__enableC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__enable_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__enable_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_enable(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__enable_retval = self.__mgr.waitForCompletion_enable(self.__enable_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__enable_retval))
                    self._get_cmd_status(self._ename, self.__enable_id, self.__enable_retval)
        self.logger.debug("enable() exit")

    # +
    # method: entercontrol()
    # -
    def entercontrol(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("entercontrol() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("entercontrol(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__entercontrolC:
                self._cname = '{0:s}_command_enterControl'.format(self._entity_lc)
                self._ename = '{0:s}_command_enterControl timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_enterControl"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_enterControlC(); data.state = 'ok')
                self.__entercontrolC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_enterControl(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__entercontrol_id = self.__mgr.issueCommand_enterControl(self.__entercontrolC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__entercontrol_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__entercontrol_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_enterControl(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__entercontrol_retval = self.__mgr.waitForCompletion_enterControl(self.__entercontrol_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__entercontrol_retval))
                    self._get_cmd_status(self._ename, self.__entercontrol_id, self.__entercontrol_retval)
        self.logger.debug("entercontrol() exit")


    # +
    # method: exitcontrol()
    # -
    def exitcontrol(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("exitcontrol() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("exitcontrol(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__exitcontrolC:
                self._cname = '{0:s}_command_exitControl'.format(self._entity_lc)
                self._ename = '{0:s}_command_exitControl timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_exitControl"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_exitControlC(); data.state = 'ok')
                self.__exitcontrolC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_exitControl(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__exitcontrol_id = self.__mgr.issueCommand_exitControl(self.__exitcontrolC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__exitcontrol_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__exitcontrol_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_exitControl(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__exitcontrol_retval = self.__mgr.waitForCompletion_exitControl(self.__exitcontrol_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__exitcontrol_retval))
                    self._get_cmd_status(self._ename, self.__exitcontrol_id, self.__exitcontrol_retval)
        self.logger.debug("exitcontrol() exit")

    # +
    # method: setvalue()
    # -
    def setvalue(self, parameter='', value='', timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("setvalue() enter, parameter={0:s}, value={1:s}, timeout={2:s}".format(parameter, value, str(timeout)))

        # check input(s)
        if not isinstance(parameter, str) or parameter == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOPAR, "parameter={0:s}".format(parameter))
        else:
            self._parameter = parameter

        if not isinstance(value, str) or value == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "value={0:s}".format(value))
        else:
            self._value = value

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("setvalue(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__setvalueC:
                self._cname = '{0:s}_command_setValue'.format(self._entity_lc)
                self._ename = '{0:s}_command_setValue parameter={1:s} value={2:s} timeout={3:d}'.format(self._entity_lc, self._parameter, self._value, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_setValue"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_setValueC(); data.state = 'ok')
                self.__setvalueC.parameter = self._parameter
                self.__setvalueC.value = self._value

                # issue command (cf. id = mgr.issueCommand_setValue(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__setvalue_id = self.__mgr.issueCommand_setValue(self.__setvalueC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__setvalue_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__setvalue_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_setValue(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__setvalue_retval = self.__mgr.waitForCompletion_setValue(self.__setvalue_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__setvalue_retval))
                    self._get_cmd_status(self._ename, self.__setvalue_id, self.__setvalue_retval)
        self.logger.debug("setvalue() exit")

    # +
    # method: standby()
    # -
    def standby(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("standby() enter, timeout={0:s}".format(str(timeout)))

        # check input(s)
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("standby(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__standbyC:
                self._cname = '{0:s}_command_standby'.format(self._entity_lc)
                self._ename = '{0:s}_command_standby timeout={1:d}'.format(self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_standby"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_standbyC(); data.state = 'ok')
                self.__standbyC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_standby(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__standby_id = self.__mgr.issueCommand_standby(self.__standbyC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__standby_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__standby_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_standby(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__standby_retval = self.__mgr.waitForCompletion_standby(self.__standby_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__standby_retval))
                    self._get_cmd_status(self._ename, self.__standby_id, self.__standby_retval)
        self.logger.debug("standby() exit")

    # +
    # method: start()
    # -
    def start(self, startid='', timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("start() enter, startid={0:s}, timeout={1:s}".format(startid, str(timeout)))

        # check input(s)
        if not isinstance(startid, str) or startid == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSID, "startid={0:s}".format(startid))
        else:
            self._startid = startid

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("start(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__startC:
                self._cname = '{0:s}_command_start'.format(self._entity_lc)
                self._ename = '{0:s}_command_start startid={1:s} timeout={2:d}'.format(self._entity_lc, self._startid, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_start"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_startC(); data.configuration = 'ok')
                self.__startC.configuration = self._startid

                # issue command (cf. id = mgr.issueCommand_start(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__start_id = self.__mgr.issueCommand_start(self.__startC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__start_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__start_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_start(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__start_retval = self.__mgr.waitForCompletion_start(self.__start_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__start_retval))
                    self._get_cmd_status(self._ename, self.__start_id, self.__start_retval)
        self.logger.debug("start() exit")

    # +
    # method: stop()
    # -
    def stop(self, device='', timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        self.logger.debug("stop() enter, device={0:s}, timeout={1:s}".format(device, str(timeout)))

        # check input(s)
        if not isinstance(device, str) or device == '':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NODEV, "device={0:s}".format(device))
        else:
            self._device = device

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("stop(), in simulation with sleep={0:s}".format(str(stime)))

        # send command
        else:
            if self.__mgr and self.__stopC:
                self._cname = '{0:s}_command_stop'.format(self._entity_lc)
                self._ename = '{0:s}_command_stop device={1:s} timeout={2:d}'.format(self._entity_lc, self._device, self._timeout)

                # set up command (cf. mgr.salCommand("camera_command_stop"))
                self.logger.debug("setting up: {0:s}".format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_stopC(); data.state = 'ok')
                self.__stopC.state = os.getenv('USER')

                # issue command (cf. id = mgr.issueCommand_stop(data))
                self.logger.debug("issuing: {0:s}".format(self._ename))
                self.__stop_id = self.__mgr.issueCommand_stop(self.__stopC)
                self.logger.debug("issued: {0:s}, id={1:d}".format(self._ename,self.__stop_id))

                # issue an event
                if self._instance_evh:
                    self._ocsid = ocs_id(False)
                    self._instance_evh.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__stop_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_stop(id, timeout))
                if self._timeout > 0:
                    self.logger.debug("waiting for: {0:s}".format(self._ename))
                    self.__stop_retval = self.__mgr.waitForCompletion_stop(self.__stop_id, self._timeout)
                    self.logger.debug("waited for: {0:s}, retval={1:d}".format(self._ename,self.__stop_retval))
                    self._get_cmd_status(self._ename, self.__stop_id, self.__stop_retval)
        self.logger.debug("stop() exit")

    # +
    # decorator(s)
    # -
    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system=''):
        self.logger.critical("system cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "system={0:s} cannot be set".format(str(system)))

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity=''):
        self.logger.critical("entity cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "entity={0:s} cannot be set".format(str(entity)))

    @property
    def simulate(self):
        return self._simulate

    @simulate.setter
    def simulate(self, simulate):
        if not isinstance(simulate, bool):
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSIM, "simulate={0:s}".format(str(simulate)))
        else:
            self._simulate = simulate

    @property
    def parameter(self):
        return self._parameter

    @parameter.setter
    def parameter(self, parameter=''):
        self.logger.critical("parameter cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "parameter={0:s} cannot be set".format(str(parameter)))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value=''):
        self.logger.critical("value cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "value={0:s} cannot be set".format(str(value)))

    @property
    def startid(self):
        return self._startid

    @startid.setter
    def startid(self, startid=''):
        self.logger.critical("startid cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "startid={0:s} cannot be set".format(str(startid)))

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device=''):
        self.logger.critical("device cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "device={0:s} cannot be set".format(str(device)))

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout=OCS_GENERIC_COMMAND_TIMEOUT):
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, "timeout={0:s}".format(timeout))
        else:
            self._timeout = timeout

    # +
    # method: __str__
    # -
    def __str__(self):
        return 'OcsGenericEntity(system=\'{0:s}\', entity=\'{1:s}\', simulate={2:s}) created at address {3:s}'.format(
            self._system, self._entity, str(self._simulate), hex(id(self)))

    # +
    # staticmethod: __dump__
    # -
    @staticmethod
    def __dump__(xv):
        if isinstance(xv, tuple) and not ():
            return ''.join("{:s}\n".format(str(v)) for v in xv)[:-1]
        elif isinstance(xv, list) and not []:
            return ''.join("{:s}\n".format(str(v)) for v in xv)[:-1]
        elif isinstance(x, dict) and not {}:
            return ''.join("{:s} : {:s}\n".format(str(k), str(v)) for k, v in xv.items())[:-1]
        else:
            return ''.join("{:s}\n".format(str(x)))


# +
# main()
# -
if __name__ == "__main__":

    camera = None
    try:
        camera = OcsGenericEntity('CCS', 'Camera', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if camera:

        # get logger
        camlog = camera.logger
        camlog.info("{0:s}".format(camera.__str__()))

        # start of night
        camlog.info("camera.entercontrol()")
        camera.entercontrol()

        camlog.info("camera.start('Normal')")
        camera.start('Normal')

        camlog.info("camera.enable()")
        camera.enable()

        # random sleep
        time.sleep(random.uniform(0, 5))

        # end of night
        camlog.info("camera.disable()")
        camera.disable()

        camlog.info("camera.standby()")
        camera.standby()

        camlog.info("camera.exitcontrol()")
        camera.exitcontrol()

        # execute destructor
        camlog.info("camera.__del__()")
        camera.__del__()

