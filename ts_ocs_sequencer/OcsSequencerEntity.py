#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "2 February 2017"
__doc__ = """Sequencer entity class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsSequencerEntity.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsSequencerEntity() inherits from the OcsGenericEntity class
# -
class OcsSequencerEntity(OcsGenericEntity):

    # +
    # method: __init__
    # -
    def __init__(self, system='OCS', entity='ocs', simulate=True):
        """
            :param system: name of system
            :param entity: name of entity
            :param simulate: if True, use simulation
            :return: None or object representing the entity
        """

        # check arguments(s)
        self._system = 'OCS'
        self._system_lc = self._system.lower()
        self._entity = 'ocs'
        self._entity_lc = self._entity.lower()
        self._simulate = simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # initialize the superclass
        super(OcsSequencerEntity, self).__init__(self._system, self._entity, self._simulate)

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None

        # container(s)
        self.__sequenceC = None
        self.__scriptC = None

        # command id(s)
        self.__sequence_id = None
        self.__script_id = None

        # return value(s)
        self.__sequence_retval = None
        self.__script_retval = None

        # other variable(s)
        self._aname = None
        self._command = None
        self._cname = None
        self._ename = None
        self._location = None
        self._mname = None
        self._timeout = OCS_SEQUENCER_COMMAND_TIMEOUT

        # import the SAL (cf. from SALPY_ocs import *)
        self._mname = 'SALPY_{0:s}'.format(self._entity)
        self.logger.debug('Importing {0:s}'.format(self._mname))
        self.__sal = ocs_sal_import(self._mname)
        if self.__sal:
            self.logger.debug('Imported {0:s} ok'.format(self._mname))

        # get mgr object (cf. mgr = SAL_ocs())
        self._aname = 'SAL_{0:s}'.format(self._entity)
        self.logger.debug('Getting attribute {0:s}'.format(self._aname))
        mgr = ocs_sal_attribute(self.__sal, self._aname)
        if mgr:
            self.__mgr = mgr()
            self.logger.debug('Got attribute {0:s} ok'.format(self._aname))

        # data structure(s) (cf. data = ocs_command_sequenceC())
        self.__sequenceC = self._get_sal_cmdC('sequence')
        self.__scriptC = self._get_sal_cmdC('script')

        # define ocs command(s) help
        self.sequencer_help = (
            'sequence system={0:s} entity={1:s} command=<string>'.format(self._system, self._entity),
            'script   system={0:s} entity={1:s} script=<string>'.format(self._system, self._entity)
            )

    # +
    # method: sequence()
    # -
    def sequence(self, command='', timeout=OCS_SEQUENCER_COMMAND_TIMEOUT):
        self.logger.debug('sequence() enter, command={0:s}, timeout={1:s}'.format(str(command), str(timeout)))

        # check input(s)
        if not isinstance(command, str) or command=='':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOCMD, 'command={0:s}'.format(command))
        else:
            self._command = command

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('sequence(), in simulation with sleep={0:s}'.format(str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__sequenceC:
                self._cname = '{0:s}_command_sequence'.format(self._entity)
                self._ename = '{0:s}_command_sequence command={1:s} timeout={2:d}'.format(self._entity, self._command, self._timeout)

                # set up command (cf. mgr.salCommand('ocs_command_sequence'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = ocs_command_sequenceC(); data.roiSpec = 'roiData')
                self.__sequenceC.command = self._command

                # issue command (cf. id = mgr.issueCommand_sequence(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__sequence_id = self.__mgr.issueCommand_sequence(self.__sequenceC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename,self.__sequence_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__sequence_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_sequence(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__sequence_retval = self.__mgr.waitForCompletion_sequence(self.__sequence_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(self._ename,self.__sequence_retval))
                    self._get_cmd_status(self._ename, self.__sequence_id, self.__sequence_retval)
        self.logger.debug('sequence() exit')

    # +
    # method: script()
    # -
    def script(self, location='', timeout=OCS_SEQUENCER_COMMAND_TIMEOUT):
        self.logger.debug('script() enter, location={0:s}, timeout={1:s}'.format(str(location), str(timeout)))

        # check input(s)
        if not isinstance(location, str) or location=='':
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOCMD, 'location={0:s}'.format(location))
        else:
            self._location = location

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('script(), in simulation with sleep={0:s}'.format(str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__scriptC:
                self._cname = '{0:s}_command_script'.format(self._entity)
                self._ename = '{0:s}_command_script location={1:s} timeout={2:d}'.format(self._entity, self._location, self._timeout)

                # set up command (cf. mgr.salCommand('ocs_command_script'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = ocs_command_scriptC(); data.roiSpec = 'roiData')
                self.__scriptC.location = self._location

                # issue command (cf. id = mgr.issueCommand_script(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__script_id = self.__mgr.issueCommand_script(self.__scriptC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename,self.__script_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.sendEvent('ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=long(self.__script_id), Identifier=float(self._ocsid), Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename, ReturnValue=long(SAL__CMD_ACK), priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_script(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__script_retval = self.__mgr.waitForCompletion_script(self.__script_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(self._ename,self.__script_retval))
                    self._get_cmd_status(self._ename, self.__script_id, self.__script_retval)
        self.logger.debug('script() exit')

    # +
    # decorator(s)
    # -
    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=''):
        self.logger.critical('command cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, 'command={0:s} cannot be set'.format(str(command)))

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location=''):
        self.logger.critical('location cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, 'location={0:s} cannot be set'.format(str(location)))


# +
# main()
# -
if __name__ == '__main__':

    sequencer = None
    try:
        sequencer = OcsSequencerEntity('OCS', 'Sequencer', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if sequencer:

        # get logger
        seqlog = sequencer.logger
        seqlog.info('{0:s}'.format(sequencer.__str__()))

        # start of night
        seqlog.info('sequencer.entercontrol()')
        sequencer.entercontrol()

        seqlog.info('sequencer.start(\'Normal\')')
        sequencer.start('Normal')

        seqlog.info('sequencer.enable()')
        sequencer.enable()

        # create an error by trying a command not available in this state
        #seqlog.info('sequencer.standby()')
        #sequencer.standby()

        # do some behavioural commands
        seqlog.info('sequencer.sequence(\'enterControl entity=camera\')')
        sequencer.sequence('enterControl entity=camera')

        seqlog.info('sequencer.sequence(\'start entity=camera startid=\'Normal\'\')')
        sequencer.sequence('start entity=camera startid=Normal')

        seqlog.info('sequencer.sequence(\'enable entity=camera\')')
        sequencer.sequence('enable entity=camera')

        # end of night
        seqlog.info('sequencer.disable()')
        sequencer.disable()

        seqlog.info('sequencer.standby()')
        sequencer.standby()

        seqlog.info('sequencer.exitcontrol()')
        sequencer.exitcontrol()

        # execute destructor
        seqlog.info('del sequencer')
        del sequencer

