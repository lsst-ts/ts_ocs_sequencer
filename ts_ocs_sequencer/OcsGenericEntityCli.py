#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
import argparse
import sys
from ocs_common import *
from OcsExceptions import *
from OcsLogger import *
from OcsGenericEntity import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Functions for manipulating command line argument(s) for generic entitites in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsGenericEntityCli.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsGenericEntityCli()
# -
class OcsGenericEntityCli(object):

    # +
    # method: __init__
    # -
    def __init__(self):
        """
            :return: None or object representing the parser
        """

        # get a logger
        self.logger = OcsLogger('OcsGenericCli', 'interpreter').logger

        # define some variables and initialize them
        self.fp = None
        self.sp = None
        self.args = None
        self.argd = None

        self.gcommands = {
            'abort' : 'Abort any running command in the commandable entity',
            'disable' : 'Disable the commandable entity',
            'enable' : 'Enable the commandable entity',
            'entercontrol' : 'Take control of the commandable entity',
            'exitcontrol' : 'Relinquish control of the commandable entity',
            'setvalue' : 'Set a parameter to a given value in the commandable entity',
            'standby' : 'Unconfigure the commandable entity',
            'start' : 'Configure the commandable entity',
            'stop' : 'Stop any running command in the commandable entity'
            }

        self.gDescription = 'Commands for commandable entity'
        self.gHelp = ''.join("{:s}\n".format(str(v)) for v in list(self.gcommands))[:-1]
        self.gUsage = 'python {0:s} <command> [<args>]\n\nGeneric command set:\n\n'.format(sys.argv[0])
        self.gCommands = ''.join("\t{:20s}{:40s}\n".format(str(k), str(v)) for k, v in self.gcommands.items())[:-1]

        self.description = self.gDescription
        self.help = self.gHelp
        self.usage = '{0:s}\n{1:s}'.format(self.gUsage,self.gCommands)


    # +
    # method: execute()
    # -
    def execute(self):
        """
            execute _setup_fp() and _parse_fp() and run command else raise exception
        """
        # set up and parse
        self._setup_fp()
        self._parse_fp()
        # if the command does not exist, raise exception otherwise execute the command
        if not hasattr(self, '_'+self.args.command):
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOCMD, "hasattr('{0:s}')".format(str(self.args.command)))
        else:
            getattr(self, '_'+self.args.command)()


    # +
    # (hidden) method: _setup_fp()
    # -
    def _setup_fp(self):
        """
            create first parse object and add postional command
        """
        self.fp = argparse.ArgumentParser(description=self.description, usage=self.usage)
        self.fp.add_argument('command', help=self.help, type=str, default='')


    # +
    # (hidden) method: _parse_fp()
    # -
    def _parse_fp(self):
        """
            parse object and get postional command from sys.argv[1:2]
        """
        self.args = self.fp.parse_args(sys.argv[1:2])
        self.logger.debug(str(self.args))


    # +
    # (hidden) method: _setup_sp()
    # -
    def _setup_sp(self,command=''):
        """
            create second parse object and add common arguments (these are required but they look optional!)
        """
        # set up parser and common command line options
        self.sp = argparse.ArgumentParser(description=self.gcommands.get(command,''))
        self.sp.add_argument('-s', '--system', type=str, help='principal subsystem', default='')
        self.sp.add_argument('-e', '--entity', type=str, help='commandable entity', default='')
        self.sp.add_argument('-m', '--simulate', type=str, help='set entity to simulate mode', default='True')
        self.sp.add_argument('-t', '--timeout', type=int, help='set entity to simulate mode', default=OCS_GENERIC_COMMAND_TIMEOUT)
        # add specific command line options
        if command == 'abort':
            pass
        elif command == 'disable':
            pass
        elif command == 'entercontrol':
            pass
        elif command == 'exitcontrol':
            pass
        elif command == 'enable':
            pass
        elif command == 'setvalue':
            self.sp.add_argument('-p', '--parameter', type=str, help='parameter name', default='')
            self.sp.add_argument('-v', '--value', type=str, help='string-encoded value', default='')
        elif command == 'standby':
            pass
        elif command == 'start':
            self.sp.add_argument('-i', '--startid', type=str, help='configuration identifier', default='')
        elif command == 'stop':
            self.sp.add_argument('-d', '--device', type=str, help='device identifier', default='')

    # +
    # (hidden) method: _parse_sp()
    # -
    def _parse_sp(self):
        """
            parse object and get arguments
        """
        # parse the command line and return the arguments namespace
        self.args = self.sp.parse_args(sys.argv[2:])
        self.logger.debug(str(self.args))

    # +
    # (hidden) method: _set_argd()
    # -
    def _set_argd(self,command):
        """
            set output dictionary, argd, from parse commands
        """
        # convert arguments namespace to dictionary
        self.argd = {}
        self.argd['command'] = command
        self.argd['system'] = self.args.system
        self.argd['entity'] = self.args.entity
        self.argd['simulate'] = self.args.simulate
        self.argd['timeout'] = self.args.timeout
        # add specific command line options
        command_lc = command.lower()
        if command_lc == 'abort':
            pass
        elif command_lc == 'disable':
            pass
        elif command_lc == 'entercontrol':
            pass
        elif command_lc == 'exitControl':
            pass
        elif command_lc == 'enable':
            pass
        elif command_lc == 'setvalue':
            self.argd['parameter'] = self.args.parameter
            self.argd['value'] = self.args.value
        elif command_lc == 'standby':
            pass
        elif command_lc == 'start':
            self.argd['startid'] = self.args.startid
        elif command_lc == 'stop':
            self.argd['device'] = self.args.device
        self.logger.debug(str(self.argd))

    # +
    # (hidden) method: abort()
    # -
    def _abort(self):
        self._setup_sp('abort')
        self._parse_sp()
        self._set_argd('abort')

    # +
    # (hidden) method: disable()
    # -
    def _disable(self):
        self._setup_sp('disable')
        self._parse_sp()
        self._set_argd('disable')

    # +
    # (hidden) method: enable()
    # -
    def _enable(self):
        self._setup_sp('enable')
        self._parse_sp()
        self._set_argd('enable')

    # +
    # (hidden) method: entercontrol()
    # -
    def _entercontrol(self):
        self._setup_sp('entercontrol')
        self._parse_sp()
        self._set_argd('entercontrol')
    def _enterControl(self):
        self.entercontrol()

    # +
    # (hidden) method: exitcontrol()
    # -
    def _exitcontrol(self):
        self._setup_sp('exitcontrol')
        self._parse_sp()
        self._set_argd('exitcontrol')
    def _exitControl(self):
        self.exitcontrol()

    # +
    # (hidden) method: setvalue()
    # -
    def _setvalue(self):
        self._setup_sp('setvalue')
        self._parse_sp()
        self._set_argd('setvalue')
    def _setValue(self):
        self.setvalue()

    # +
    # (hidden) method: standby()
    # -
    def _standby(self):
        self._setup_sp('standby')
        self._parse_sp()
        self._set_argd('standby')

    # +
    # (hidden) method: start()
    # -
    def _start(self):
        self._setup_sp('start')
        self._parse_sp()
        self._set_argd('start')

    # +
    # (hidden) method: stop()
    # -
    def _stop(self):
        self._setup_sp('stop')
        self._parse_sp()
        self._set_argd('stop')


# +
# main()
# -
if __name__ == '__main__':

    # get a command line parser
    gencli = None
    try:
        gencli = OcsGenericEntityCli()
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the parser and set some defaults
    if gencli:
        gencli.execute()
        system = gencli.argd.get('system','')
        entity = gencli.argd.get('entity','').lower()
        simulate = gencli.argd.get('simulate','')
        if simulate.lower() == 'true':
            simulate = True
        else:
            simulate = False
        command = gencli.argd.get('command','')
        timeout = gencli.argd.get('timeout',OCS_GENERIC_COMMAND_TIMEOUT)

    # get a generic entity object
    genobj = None
    try:
        genobj = OcsGenericEntity(system, entity, simulate)
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the given command
    if genobj:

        command_lc = command.lower()
        if command_lc == 'abort':
            try:
                genobj.abort(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'disable':
            try:
                genobj.disable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'enable':
            try:
                genobj.enable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'entercontrol':
            try:
                genobj.entercontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'exitcontrol':
            try:
                genobj.exitcontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'setvalue':
            parameter = gencli.argd.get('parameter','')
            value = gencli.argd.get('value','')
            try:
                genobj.setvalue(parameter, value, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'standby':
            try:
                genobj.standby(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'start':
            startid = gencli.argd.get('startid','')
            try:
                genobj.start(startid, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'stop':
            device = gencli.argd.get('device','')
            try:
                genobj.stop(device, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)
