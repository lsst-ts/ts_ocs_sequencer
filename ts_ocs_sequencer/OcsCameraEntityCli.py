#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntityCli import *
from OcsCameraEntity import *

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Class for manipulating command line argument(s) for the camera entity in the OCS"""
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
            'initGuiders' : 'Initialize the guiders',
            'initImage' : 'Initialize the image acquisition',
            'setFilter' : 'Set filter into beam',
            'takeImages' : 'Take a number of exposures',
            'clear' : 'Clear the focal plane',
            'discardRows' : 'Discard a number of rows within each image whilst integrating',
            'endImage' : 'Terminate open-ended image acquisition',
            'startImage' : 'Open-ended start image acquisition'
            }

        self.bHelp = ''.join("{:s}\n".format(str(v)) for v in list(self.bcommands))[:-1]
        self.bCommands = ''.join("\t{:20s}{:40s}\n".format(str(k), str(v)) for k, v in self.bcommands.items())[:-1]
        self.bUsage = 'Behavioural command set:\n\n'

        self.help = '{0:s}\n\n{1:s}'.format(self.gHelp,self.bHelp)
        self.usage = '{0:s}\n{1:s}\n\n{2:s}\n{3:s}'.format(self.gUsage,self.gCommands,self.bUsage,self.bCommands)


    # +
    # (override hidden) method: _set_argd()
    # -
    def _set_argd(self,command):
        # execute the superclass function
        super(OcsCameraCli, self)._set_argd(command)
        command_lc = command.lower()
        if command_lc == 'clear':
            self.argd['nclear'] = self.args.nclear
        elif command_lc == 'discardrows':
            self.argd['rows'] = self.args.rows
        elif command_lc == 'endImage':
            pass
        elif command_lc == 'initguiders':
            self.argd['roispec'] = self.args.roispec
        elif command_lc == 'initimage':
            self.argd['deltat'] = self.args.deltat
        elif command_lc == 'setfilter':
            self.argd['name'] = self.args.name
        elif command_lc == 'startimage':
            self.argd['shutter'] = self.args.shutter
            self.argd['science'] = self.args.science
            self.argd['guide'] = self.args.guide
            self.argd['wfs'] = self.args.wfs
            self.argd['imagesequencename'] = self.args.imagesequencename
        elif command_lc == 'takeimages':
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
    def _discardRows(self):
        self._setup_sp('discardRows')
        self.sp.add_argument('-r', '--rows', type=int, help='number of rows', default=0)
        self._parse_sp()
        self._set_argd('discardRows')
    def _discardrows(self):
        self._discardRows()


    # +
    # (hidden) method: _endImage()
    # -
    def _endImage(self):
        self._setup_sp('endImage')
        self._parse_sp()
        self._set_argd('endImage')
    def _endimage(self):
        self._endImage()


    # +
    # (hidden) method: _initGuiders()
    # -
    def _initGuiders(self):
        self._setup_sp('initGuiders')
        self.sp.add_argument('-r', '--roispec', type=str, help='region-of-interest specification', default='')
        self._parse_sp()
        self._set_argd('initGuiders')
    def _initguiders(self):
        self._initGuiders()


    # +
    # (hidden) method: _initImage()
    # -
    def _initImage(self):
        self._setup_sp('initImage')
        self.sp.add_argument('-d', '--deltat', type=float, help='delta time', default=0.0)
        self._parse_sp()
        self._set_argd('initImage')
    def _initimage(self):
        self._initImage()


    # +
    # (hidden) method: _setFilter()
    # -
    def _setFilter(self):
        self._setup_sp('setFilter')
        self.sp.add_argument('-n', '--name', type=str, help='filter name', default='')
        self._parse_sp()
        self._set_argd('setFilter')
    def _setfilter(self):
        self._setFilter()


    # +
    # (hidden) method: _startImage()
    # -
    def _startImage(self):
        self._setup_sp('startImage')
        self.sp.add_argument('-u', '--shutter', type=str, help='shutter state', default='')
        self.sp.add_argument('-c', '--science', type=str, help='science area state', default='')
        self.sp.add_argument('-g', '--guide', type=str, help='guider state', default='')
        self.sp.add_argument('-w', '--wfs', type=str, help='wavefront sensor state', default='')
        self.sp.add_argument('-i', '--imagesequencename', type=str, help='image sequence name', default='')
        self._parse_sp()
        self._set_argd('startImage')
    def _startimage(self):
        self._startImage()


    # +
    # (hidden) method: _takeImages()
    # -
    def _takeImages(self):
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
    def _takeimages(self):
        self._takeImages()


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
        system = camcli.argd.get('system','')
        entity = camcli.argd.get('entity','').lower()
        simulate = camcli.argd.get('simulate','')
        if simulate.lower() == 'true':
            simulate = True
        else:
            simulate = False
        command = camcli.argd.get('command','')
        timeout = camcli.argd.get('timeout',OCS_GENERIC_COMMAND_TIMEOUT)

    # get a generic entity object
    camera = None
    try:
        camera = OcsCameraEntity(system, entity, simulate)
    except OcsGenericEntityException as e:
        print(e.errstr)

    # execute the given command
    if camera:

        command_lc = command.lower()
        if command_lc == 'abort':
            try:
                camera.abort(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'disable':
            try:
                camera.disable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'enable':
            try:
                camera.enable(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'entercontrol':
            try:
                camera.entercontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'exitcontrol':
            try:
                camera.exitcontrol(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'setvalue':
            parameter = camcli.argd.get('parameter','')
            value = camcli.argd.get('value','')
            try:
                camera.setvalue(parameter, value, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'standby':
            try:
                camera.standby(timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'start':
            startid = camcli.argd.get('startid','')
            try:
                camera.start(startid, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'stop':
            device = camcli.argd.get('device','')
            try:
                camera.stop(device, timeout)
            except OcsGenericEntityException as e:
                print(e.errstr)

        elif command_lc == 'clear':
            nclear = int(camcli.argd.get('nclear', 0))
            try:
                camera.clear(nclear, timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'discardrows':
            nrows = int(camcli.argd.get('rows', 0))
            try:
                camera.discardRows(rows, timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'endimage':
            try:
                camera.endImage(timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'initguiders':
            roispec = camcli.argd.get('roispec','')
            try:
                camera.initGuiders(roispec, timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'initimage':
            deltat = float(camcli.argd.get('deltat', 0.0))
            try:
                camera.initImage(deltat, timeout)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'setfilter':
            name = camcli.argd.get('name','')
            try:
                camera.setFilter(name, 60)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'startimage':
            shutter = bool(camcli.argd.get('shutter',True))
            science = bool(camcli.argd.get('science',True))
            guide = bool(camcli.argd.get('guide',False))
            wfs = bool(camcli.argd.get('wfs',False))
            imageSequenceName = camcli.argd.get('imagesequencename','')
            try:
                camera.startImage(shutter, science, guide, wfs, imageSequenceName, 60)
            except OcsCameraEntityException as e:
                print(e.errstr)

        elif command_lc == 'takeimages':
            numImages = int(camcli.argd.get('numimages', 0))
            expTime = float(camcli.argd.get('exptime', 0.0))
            shutter = bool(camcli.argd.get('shutter', True))
            science = bool(camcli.argd.get('science', True))
            guide = bool(camcli.argd.get('guide', False))
            wfs = bool(camcli.argd.get('wfs', False))
            imageSequenceName = camcli.argd.get('imagesequencename','')
            try:
                camera.takeImages(numImages, expTime, shutter, science, guide, wfs, imageSequenceName, 40)
            except OcsCameraEntityException as e:
                print(e.errstr)

