#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *
from OcsCameraEntity import *


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py, contains the code for command line functionality
for any generic commandable entities. Python (unit) tests are in $TS_OCS_SEQUENCER_TESTS/test_OcsCameraEntityCli.py.

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.

API:

    None

CLI:

    This class inherits from $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py and, therefore, acquires all
    the CLI methods therein. It also implements the following behavioural CLI:

    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py takeimages --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-n NUMIMAGES] [-x EXPTIME]
                                 [-u SHUTTER] [-c SCIENCE] [-g GUIDE] [-w WFS]
                                 [-i IMAGESEQUENCENAME]
    
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
      -n NUMIMAGES, --numimages NUMIMAGES
                            number of exposures
      -x EXPTIME, --exptime EXPTIME
                            exposure time
      -u SHUTTER, --shutter SHUTTER
                            shutter state
      -c SCIENCE, --science SCIENCE
                            science area state
      -g GUIDE, --guide GUIDE
                            guider state
      -w WFS, --wfs WFS     wavefront sensor state
      -i IMAGESEQUENCENAME, --imagesequencename IMAGESEQUENCENAME
                            image sequence name
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py setfilter --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-n NAME]
    
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
      -n NAME, --name NAME  filter name
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py initguiders --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-r ROISPEC]
    
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
      -r ROISPEC, --roispec ROISPEC
                            region-of-interest specification
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py initimage --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-d DELTAT]
    
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
      -d DELTAT, --deltat DELTAT
                            delta time
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py clear --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-n NCLEAR]
    
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
      -n NCLEAR, --nclear NCLEAR
                            number of clears
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py discardrows --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-r ROWS]
    
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
      -r ROWS, --rows ROWS  number of rows
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py endimage --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT]
    
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
    
    % python $TS_OCS_SEQUENCER/OcsCameraEntityCli.py startimage --help
    usage: OcsCameraEntityCli.py [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE]
                                 [-t TIMEOUT] [-u SHUTTER] [-c SCIENCE] [-g GUIDE]
                                 [-w WFS] [-i IMAGENAME]
    
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
      -u SHUTTER, --shutter SHUTTER
                            shutter state
      -c SCIENCE, --science SCIENCE
                            science area state
      -g GUIDE, --guide GUIDE
                            guider state
      -w WFS, --wfs WFS     wavefront sensor state
      -i IMAGENAME, --imagename IMAGENAME
                            image name
"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "OcsCameraEntityCli.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsCameraCli() inherits from the OcsGenericEntityCli class
# -
class OcsCameraCli(OcsGenericEntityCli):

    def __init__(self):

        # initialize the superclass
        super(OcsCameraCli, self).__init__()

        # define some variables and initialize them
        self.bcommands = {
            'initGuiders': 'Initialize the guiders',
            'initImage': 'Initialize the image acquisition',
            'setFilter': 'Set filter into beam',
            'takeImages': 'Take a number of exposures',
            'clear': 'Clear the focal plane',
            'discardRows': 'Discard a number of rows within each image whilst integrating',
            'endImage': 'Terminate open-ended image acquisition',
            'startImage': 'Open-ended start image acquisition'
            }

        self.bHelp = ''.join("{:s}\n".format(str(v)) for v in list(self.bcommands))[:-1]
        self.bCommands = ''.join("\t{:20s}{:40s}\n".format(str(k), str(v)) for k, v in self.bcommands.items())[:-1]
        self.bUsage = 'Behavioural command set:\n\n'

        self.help = '{0:s}\n\n{1:s}'.format(self.gHelp, self.bHelp)
        self.usage = '{0:s}\n{1:s}\n\n{2:s}\n{3:s}'.format(self.gUsage, self.gCommands, self.bUsage, self.bCommands)

    # +
    # (override hidden) method: _set_argd()
    # -
    def _set_argd(self, cmd=''):
        # execute the superclass function
        super(OcsCameraCli, self)._set_argd(cmd)
        cmd_lc = cmd.lower()
        if cmd_lc == 'clear':
            self.argd['nclear'] = self.args.nclear
        elif cmd_lc == 'discardrows':
            self.argd['rows'] = self.args.rows
        elif cmd_lc == 'endimage':
            pass
        elif cmd_lc == 'initguiders':
            self.argd['roispec'] = self.args.roispec
        elif cmd_lc == 'initimage':
            self.argd['deltat'] = self.args.deltat
        elif cmd_lc == 'setfilter':
            self.argd['name'] = self.args.name
        elif cmd_lc == 'startimage':
            self.argd['shutter'] = self.args.shutter
            self.argd['science'] = self.args.science
            self.argd['guide'] = self.args.guide
            self.argd['wfs'] = self.args.wfs
            self.argd['imagename'] = self.args.imagename
        elif cmd_lc == 'takeimages':
            self.argd['numimages'] = self.args.numimages
            self.argd['exptime'] = self.args.exptime
            self.argd['shutter'] = self.args.shutter
            self.argd['science'] = self.args.science
            self.argd['guide'] = self.args.guide
            self.argd['wfs'] = self.args.wfs
            self.argd['imagesequencename'] = self.args.imagesequencename
        self.logger.debug(str(self.argd))

    # +
    # (hidden) method: _clear()
    # -
    def _clear(self):
        self._setup_sp('clear')
        self.sp.add_argument('-n', '--nclear', type=int, help='number of clears', default=0)
        self._parse_sp()
        self._set_argd('clear')

    # +
    # (hidden) method: _discardRows()
    # -
    def _discardrows(self):
        self._setup_sp('discardRows')
        self.sp.add_argument('-r', '--rows', type=int, help='number of rows', default=0)
        self._parse_sp()
        self._set_argd('discardRows')

    # +
    # (hidden) method: _endImage()
    # -
    def _endimage(self):
        self._setup_sp('endImage')
        self._parse_sp()
        self._set_argd('endImage')

    # +
    # (hidden) method: _initGuiders()
    # -
    def _initguiders(self):
        self._setup_sp('initGuiders')
        self.sp.add_argument('-r', '--roispec', type=str, help='region-of-interest specification', default='')
        self._parse_sp()
        self._set_argd('initGuiders')

    # +
    # (hidden) method: _initImage()
    # -
    def _initimage(self):
        self._setup_sp('initImage')
        self.sp.add_argument('-d', '--deltat', type=float, help='delta time', default=0.0)
        self._parse_sp()
        self._set_argd('initImage')

    # +
    # (hidden) method: _setFilter()
    # -
    def _setfilter(self):
        self._setup_sp('setFilter')
        self.sp.add_argument('-n', '--name', type=str, help='filter name', default='')
        self._parse_sp()
        self._set_argd('setFilter')

    # +
    # (hidden) method: _startImage()
    # -
    def _startimage(self):
        self._setup_sp('startImage')
        self.sp.add_argument('-u', '--shutter', type=str, help='shutter state', default='')
        self.sp.add_argument('-c', '--science', type=str, help='science area state', default='')
        self.sp.add_argument('-g', '--guide', type=str, help='guider state', default='')
        self.sp.add_argument('-w', '--wfs', type=str, help='wavefront sensor state', default='')
        self.sp.add_argument('-i', '--imagename', type=str, help='image name', default='')
        self._parse_sp()
        self._set_argd('startImage')

    # +
    # (hidden) method: _takeImages()
    # -
    def _takeimages(self):
        self._setup_sp('takeImages')
        self.sp.add_argument('-n', '--numimages', type=int, help='number of exposures', default=0)
        self.sp.add_argument('-x', '--exptime', type=float, help='exposure time', default=0.0)
        self.sp.add_argument('-u', '--shutter', type=bool, help='shutter state', default='Closed')
        self.sp.add_argument('-c', '--science', type=bool, help='science area state', default='')
        self.sp.add_argument('-g', '--guide', type=bool, help='guider state', default='')
        self.sp.add_argument('-w', '--wfs', type=bool, help='wavefront sensor state', default='')
        self.sp.add_argument('-i', '--imagesequencename', type=str, help='image sequence name', default=ocs_id(True))
        self._parse_sp()
        self._set_argd('takeImages')


# +
# main()
# -
if __name__ == '__main__':

    # get a command line parser
    camcli = None
    try:
        camcli = OcsCameraCli()
    except OcsCameraEntityException as e:
        print(e.errstr)
    except OcsGenericEntityException as f:
        print(f.errstr)

    # execute the parser and set some defaults
    if camcli:
        camcli.execute()
        _system = camcli.argd.get('system', '')
        _entity = camcli.argd.get('entity', '').lower()
        _simulate = camcli.argd.get('simulate', '')
        if _simulate.lower() == 'true':
            _simulate = True
        else:
            _simulate = False
        _command = camcli.argd.get('command', '')
        _timeout = camcli.argd.get('timeout', OCS_GENERIC_COMMAND_TIMEOUT)
    else:
        _system = 'CCS'
        _entity = 'Camera'
        _simulate = True
        _command = ''
        _timeout = OCS_GENERIC_COMMAND_TIMEOUT

    # get a generic entity object
    camera = None
    try:
        camera = OcsCameraEntity(_system, _entity, _simulate)
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the given command
    if camera:

        command_lc = _command.lower()
        if command_lc == 'abort':
            try:
                camera.abort(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'disable':
            try:
                camera.disable(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'enable':
            try:
                camera.enable(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'entercontrol':
            try:
                camera.entercontrol(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'exitcontrol':
            try:
                camera.exitcontrol(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'setvalue':
            parameter = camcli.argd.get('parameter', '')
            value = camcli.argd.get('value', '')
            try:
                camera.setvalue(parameter, value, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'standby':
            try:
                camera.standby(_timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'start':
            startid = camcli.argd.get('startid', '')
            try:
                camera.start(startid, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'stop':
            device = camcli.argd.get('device', '')
            try:
                camera.stop(device, _timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'clear':
            nclear = int(camcli.argd.get('nclear', 0))
            try:
                camera.clear(nclear, _timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'discardrows':
            _nrows = int(camcli.argd.get('rows', 0))
            try:
                camera.discard_rows(_nrows, _timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'endimage':
            try:
                camera.end_image(_timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'initguiders':
            _roispec = camcli.argd.get('roispec', '')
            try:
                camera.init_guiders(_roispec, _timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'initimage':
            _deltat = float(camcli.argd.get('deltat', 0.0))
            try:
                camera.init_image(_deltat, _timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'setfilter':
            _name = camcli.argd.get('name', '')
            try:
                camera.set_filter(_name, 60)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'startimage':
            _shutter = bool(camcli.argd.get('shutter', True))
            _science = bool(camcli.argd.get('science', True))
            _guide = bool(camcli.argd.get('guide', False))
            _wfs = bool(camcli.argd.get('wfs', False))
            _imagename = camcli.argd.get('imagename', '')
            try:
                camera.start_image(_shutter, _science, _guide, _wfs, _imagename, 60)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'take_images':
            _numimages = int(camcli.argd.get('numimages', 0))
            _exptime = float(camcli.argd.get('exptime', 0.0))
            _shutter = bool(camcli.argd.get('shutter', True))
            _science = bool(camcli.argd.get('science', True))
            _guide = bool(camcli.argd.get('guide', False))
            _wfs = bool(camcli.argd.get('wfs', False))
            _imagesequencename = camcli.argd.get('imagesequencename', '')
            try:
                camera.take_images(_numimages, _exptime, _shutter, _science, _guide, _wfs, _imagesequencename, 40)
            except OcsCameraEntityException as e:
                print(e.errstr)
