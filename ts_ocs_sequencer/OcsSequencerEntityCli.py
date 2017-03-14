#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *
from OcsSequencerEntity import *


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py, contains the code for command line functionality
for any generic commandable entities. Python (unit) tests are in $TS_OCS_SEQUENCER_TESTS/test_OcsSequencerEntityCli.py.

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.

API:

    None

CLI:

    This class inherits from $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py and, therefore, acquires all
    the CLI methods therein. It also implements the following behavioural CLI:

    % python $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py sequence --help
    usage: OcsSequencerEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                    [-t TIMEOUT] [-q SEQCMD]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SYSTEM, --system SYSTEM
                            principal subsystem
      -e ENTITY, --entity ENTITY
                            commandable entity
      -m SIMULATE, --simulate SIMULATE
                            set entity to simulate mode
      -t TIMEOUT, --timeout TIMEOUT
                            set entity to simulate mode
      -q SEQCMD, --seqcmd SEQCMD
                            command to sequence
    
    % python $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py script --help
    usage: OcsSequencerEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                [-t TIMEOUT] [-p SCRIPT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SYSTEM, --system SYSTEM
                            principal subsystem
      -e ENTITY, --entity ENTITY
                            commandable entity
      -m SIMULATE, --simulate SIMULATE
                            set entity to simulate mode
      -t TIMEOUT, --timeout TIMEOUT
                            set entity to simulate mode
      -p SCRIPT, --script SCRIPT
                            script to run
"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "14 February 2017"
__email__ = "pdaly@lsst.org"
__file__ = "OcsSequencerEntityCli.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsSequencerCli() inherits from the OcsGenericEntityCli class
# -
class OcsSequencerCli(OcsGenericEntityCli):

    def __init__(self):

        # initialize the superclass
        super(OcsSequencerCli, self).__init__()

        # define some variables and initialize them
        self.bcommands = {
            'sequence': 'Send sequence to other entity',
            'script': 'Run script'
            }

        self.bHelp = ''.join("{:s}\n".format(str(v)) for v in list(self.bcommands))[:-1]
        self.bCommands = ''.join("\t{:20s}{:40s}\n".format(str(k), str(v)) for k, v in self.bcommands.items())[:-1]
        self.bUsage = 'Behavioural command set:\n\n'

        self.help = '{0:s}\n\n{1:s}'.format(self.gHelp, self.bHelp)
        self.usage = '{0:s}\n{1:s}\n\n{2:s}\n{3:s}'.format(self.gUsage, self.gCommands, self.bUsage, self.bCommands)

    # +
    # (override hidden) method: _set_argd()
    # -
    def _set_argd(self, incmd):
        # execute the superclass function
        super(OcsSequencerCli, self)._set_argd(incmd)
        incmd_lc = incmd.lower()
        if incmd_lc == 'sequence':
            self.argd['seqcmd'] = self.args.seqcmd
        elif incmd_lc == 'script':
            self.argd['location'] = self.args.script
        self.logger.debug(str(self.argd))

    # +
    # (hidden) method: _sequence()
    # -
    def _sequence(self):
        self._setup_sp('sequence')
        self.sp.add_argument('-q', '--seqcmd', type=str, help='command to sequence', default='')
        self._parse_sp()
        self._set_argd('sequence')

    # +
    # (hidden) method: _script()
    # -
    def _script(self):
        self._setup_sp('script')
        self.sp.add_argument('-p', '--script', type=str, help='script to run', default='')
        self._parse_sp()
        self._set_argd('script')


# +
# main()
# -
if __name__ == '__main__':

    # get a command line parser
    seqcli = None
    try:
        seqcli = OcsSequencerCli()
    except OcsSequencerEntityException as e:
        print(e.errstr)
    except OcsGenericEntityException as f:
        print(f.errstr)

    # execute the parser and set some defaults
    if seqcli:
        seqcli.execute()
        _system = seqcli.argd.get('system', '')
        _entity = seqcli.argd.get('entity', '').lower()
        _simulate = seqcli.argd.get('simulate', '')
        if _simulate.lower() == 'true':
            _simulate = True
        else:
            _simulate = False
        _command = seqcli.argd.get('command', '')
        _timeout = seqcli.argd.get('timeout', OCS_GENERIC_COMMAND_TIMEOUT)
    else:
        _system = 'OCS'
        _entity = 'Sequencer'
        _simulate = True
        _command = ''
        _timeout = OCS_GENERIC_COMMAND_TIMEOUT

    # get a generic entity object
    sequencer = None
    try:
        sequencer = OcsSequencerEntity(_system, _entity, _simulate)
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the given command
    if sequencer:

        command_lc = _command.lower()
        if command_lc == 'abort':
            try:
                sequencer.abort(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'disable':
            try:
                sequencer.disable(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'enable':
            try:
                sequencer.enable(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'entercontrol':
            try:
                sequencer.entercontrol(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'exitcontrol':
            try:
                sequencer.exitcontrol(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'setvalue':
            parameter = seqcli.argd.get('parameter', '')
            value = seqcli.argd.get('value', '')
            try:
                sequencer.setvalue(parameter, value, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'standby':
            try:
                sequencer.standby(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'start':
            startid = seqcli.argd.get('startid', '')
            try:
                sequencer.start(startid, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'stop':
            device = seqcli.argd.get('device', '')
            try:
                sequencer.stop(device, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'sequence':
            cmd = seqcli.argd.get('command', '')
            try:
                sequencer.sequence(cmd, _timeout)
            except OcsSequencerEntityException as e:
                print(e.errstr)

        elif command_lc == 'script':
            script = seqcli.argd.get('location', '')
            try:
                sequencer.script(script, _timeout)
            except OcsSequencerEntityException as e:
                print(e.errstr)
