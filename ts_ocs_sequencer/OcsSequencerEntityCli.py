#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *
from OcsSequencerEntity import *

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "14 February 2017"
__doc__ = """Class for manipulating command line argument(s) for the sequencer entity in the OCS"""
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
            'sequence' : 'Send sequence to other entity',
            'script' : 'Run script',
            'shutdown' : 'Set flag to shutdown entity',
            }

        self.bHelp = ''.join("{:s}\n".format(str(v)) for v in list(self.bcommands))[:-1]
        self.bCommands = ''.join("\t{:20s}{:40s}\n".format(str(k), str(v)) for k, v in self.bcommands.items())[:-1]
        self.bUsage = 'Behavioural command set:\n\n'

        self.help = '{0:s}\n\n{1:s}'.format(self.gHelp,self.bHelp)
        self.usage = '{0:s}\n{1:s}\n\n{2:s}\n{3:s}'.format(self.gUsage,self.gCommands,self.bUsage,self.bCommands)


    # +
    # (override hidden) method: _set_argd()
    # -
    def _set_argd(self, command):
        # execute the superclass function
        super(OcsSequencerCli, self)._set_argd(command)
        command_lc = command.lower()
        if command_lc == 'sequence':
            self.argd['seqcmd'] = self.args.seqcmd
        elif command_lc == 'script':
            self.argd['location'] = self.args.script
        elif command_lc == 'shutdown':
            pass
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
        self.sp.add_argument('-s', '--script', type=str, help='script to run', default='')
        self._parse_sp()
        self._set_argd('script')


    # +
    # (hidden) method: _shutdown()
    # -
    def _shutdown(self):
        self._setup_sp('shutdown')
        self._parse_sp()
        self._set_argd('shutdown')


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
        system = seqcli.argd.get('system','')
        entity = seqcli.argd.get('entity','').lower()
        simulate = seqcli.argd.get('simulate','')
        if simulate.lower() == 'true':
            simulate = True
        else:
            simulate = False
        command = seqcli.argd.get('command','')
        timeout = seqcli.argd.get('timeout',OCS_GENERIC_COMMAND_TIMEOUT)

    # get a generic entity object
    sequencer = None
    try:
        sequencer = OcsSequencerEntity(system, entity, simulate)
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the given command
    if sequencer:

        command_lc = command.lower()
        if command_lc == 'abort':
            try:
                sequencer.abort(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'disable':
            try:
                sequencer.disable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'enable':
            try:
                sequencer.enable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'entercontrol':
            try:
                sequencer.entercontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'exitcontrol':
            try:
                sequencer.exitcontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'setvalue':
            parameter = seqcli.argd.get('parameter','')
            value = seqcli.argd.get('value','')
            try:
                sequencer.setvalue(parameter, value, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'standby':
            try:
                sequencer.standby(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'start':
            startid = seqcli.argd.get('startid','')
            try:
                sequencer.start(startid, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'stop':
            device = seqcli.argd.get('device','')
            try:
                sequencer.stop(device, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'sequence':
            cmd = seqcli.argd.get('command', '')
            try:
                sequencer.sequence(cmd, timeout)
            except OcsSequencerEntityException as e:
                print(e.errstr)

        elif command_lc == 'script':
            script = seqcli.argd.get('location', '')
            try:
                sequencer.discardRows(script, timeout)
            except OcsSequencerEntityException as e:
                print(e.errstr)

        elif command_lc == 'shutdown':
            try:
                sequencer.shutdown(timeout)
            except OcsSequencerEntityException as e:
                print(e.errstr)

