#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *
from ocs_id import *
from ocs_sal_constants import *


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsCameraEntity.py, contains the code for OCS access to the camera
commandable entity. Python (unit) tests are in $TS_OCS_SEQUENCER_TESTS/test_OcsCameraEntity.py.

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.


Example:

    camera = None
    try:
        camera = OcsCameraEntity('DMCS', 'Archiver', True)
    except OcsCameraEntityException as e:
        print(e.errstr)
    if camera:
        camera.entercontrol()

API:

    OcsCameraEntity(system='', entity='', simulation=True)
        class initializes a given sub-system and entity with simulation mode enabled (True) or
        disabled (False). If the object cannot be instantiated, an OcsCameraEntityException will
        be raised.

    The OcsCameraEntity class provides the following (public) methods:

        abort(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic abort() command. If timeout > 0, the method waits for completion.
        disable(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic disable() command. If timeout > 0, the method waits for completion.
        enable(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic enable() command. If timeout > 0, the method waits for completion.
        entercontrol(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic enterControl() command. If timeout > 0, the method waits for completion.
        exitcontrol(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic exitControl() command. If timeout > 0, the method waits for completion.
        setvalue(parameter='', value='', timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic setValue() command. If timeout > 0, the method waits for completion.
        standby(timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic standby() command. If timeout > 0, the method waits for completion.
        start(startid='', timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic start() command. If timeout > 0, the method waits for completion.
        stop(device='', timeout=OCS_GENERIC_COMMAND_TIMEOUT)
            sends a generic stop() command. If timeout > 0, the method waits for completion.

        init_guiders(self, roispec='', timeout=OCS_CAMERA_COMMAND_TIMEOUT)
            send a behavioural initGuiders() command. If timeout > 0, the method waits for completion.
            The roispec argument contains the format of the `region-of-interest.
        init_image(self, deltat=0.0, timeout=OCS_CAMERA_COMMAND_TIMEOUT)
            send a behavioural initImage() command. If timeout > 0, the method waits for completion.
            The deltat argument provides the estimate of the shutter opening time.
        set_filter(self, name='', timeout=OCS_CAMERA_FILTER_COMMAND_TIMEOUT)
            send a behavioural setFilter() command. If timeout > 0, the method waits for completion.
            The name argument selects the desired filter to place in the beam.
        take_images(self, numimages=-1, exptime=-1.0, shutter=False, science=False, guide=False, wfs=False, imageSequenceName='')
            send a behavioural takeImages() command. If timeout > 0, the method waits for completion.
            The arguments specify the data acquisition:
                numImage = number of images to capture
                expTime = the exposure time per image
                shutter = open (True) or close (False) the shutter during integration
                science = science arrays are active (True) or inactive (False) during integration
                guide = guiders are active (True) or inactive (False) during integration
                wfs = wave front sensors are active (True) or inactive (False) during integration
                imageSequenceName = the (root) image name to use during a sequence
        clear(self, nclear=0, timeout=OCS_CAMERA_COMMAND_TIMEOUT)
            send a behavioural clear() command. If timeout > 0, the method waits for completion.
            The nClear argument specifies how many clears to perform.
        discard_rows(self, nrows=0, timeout=OCS_CAMERA_COMMAND_TIMEOUT)
            send a behavioural discard_rows() command. If timeout > 0, the method waits for completion.
            The nRows argument specifies how many rows to discard.
        end_image(self, timeout=OCS_CAMERA_COMMAND_TIMEOUT)
            send a behavioural endImage() command. If timeout > 0, the method waits for completion.
            This command stops a previously issued, and open ended, startImage() command
        start_image(self, shutter=False, science=False, guide=False, wfs=False, imageName='')
            send a behavioural startImage() command. If timeout > 0, the method waits for completion.
            The arguments specify the (open ended) data acquisition:
                shutter = open (True) or close (False) the shutter during integration
                science = science arrays are active (True) or inactive (False) during integration
                guide = guiders are active (True) or inactive (False) during integration
                wfs = wave front sensors are active (True) or inactive (False) during integration
                imageSequenceName = the (root) image name to use during a sequence

CLI 

    The command line interface is provided in a separate class. 
    See $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py for details.

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "OcsCameraEntity.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsCameraEntity() inherits from the OcsGenericEntity class
# -
class OcsCameraEntity(OcsGenericEntity):

    # +
    # method: __init__
    # -
    def __init__(self, system='CCS', entity='Camera', simulate=True):
        """
            :param system: name of system
            :param entity: name of entity
            :param simulate: if True, use simulation
            :return: None or object representing the entity
        """

        # check arguments(s)
        self._system = system
        self._system_lc = self._system.lower()
        self._entity = entity
        self._entity_lc = self._entity.lower()
        self._simulate = simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # initialize the superclass
        super(OcsCameraEntity, self).__init__(self._system, self._entity, self._simulate)

        # declare some variables and initialize them
        self.__sal = None
        self.__mgr = None

        # container(s)
        self.__initGuidersC = None
        self.__initImageC = None
        self.__setFilterC = None
        self.__takeImagesC = None
        self.__clearC = None
        self.__discardRowsC = None
        self.__endImageC = None
        self.__startImageC = None

        # command id(s)
        self.__initGuiders_id = None
        self.__initImage_id = None
        self.__setFilter_id = None
        self.__takeImages_id = None
        self.__clear_id = None
        self.__discardRows_id = None
        self.__endImage_id = None
        self.__startImage_id = None

        # return value(s)
        self.__initGuiders_retval = None
        self.__initImage_retval = None
        self.__setFilter_retval = None
        self.__takeImages_retval = None
        self.__clear_retval = None
        self.__discardRows_retval = None
        self.__endImage_retval = None
        self.__startImage_retval = None

        # other variable(s)
        self._aname = None
        self._cname = None
        self._deltat = None
        self._ename = None
        self._exptime = None
        self._guide = None
        self._imagename = None
        self._imagesequencename = None
        self._mname = None
        self._name = None
        self._nclear = None
        self._nrows = None
        self._numimages = None
        self._roispec = None
        self._science = None
        self._shutter = None
        self._timeout = OCS_CAMERA_COMMAND_TIMEOUT
        self._wfs = None

        # import the SAL (cf. from SALPY_camera import *)
        self._mname = 'SALPY_{0:s}'.format(self._entity_lc)
        self.logger.debug('Importing {0:s}'.format(self._mname))
        self.__sal = ocs_sal_import(self._mname)
        if self.__sal:
            self.logger.debug('Imported {0:s} ok'.format(self._mname))

        # get mgr object (cf. mgr = SAL_camera())
        self._aname = 'SAL_{0:s}'.format(self._entity_lc)
        self.logger.debug('Getting attribute {0:s}'.format(self._aname))
        mgr = ocs_sal_attribute(self.__sal, self._aname)
        if mgr:
            self.__mgr = mgr()
            self.logger.debug('Got attribute {0:s} ok'.format(self._aname))

        # data structure(s) (cf. data = camera_command_initGuidersC())
        self.__initGuidersC = self._get_sal_cmd_container('initGuiders')
        self.__initImageC = self._get_sal_cmd_container('initImage')
        self.__setFilterC = self._get_sal_cmd_container('setFilter')
        self.__takeImagesC = self._get_sal_cmd_container('takeImages')
        self.__clearC = self._get_sal_cmd_container('clear')
        self.__discardRowsC = self._get_sal_cmd_container('discardRows')
        self.__endImageC = self._get_sal_cmd_container('endImage')
        self.__startImageC = self._get_sal_cmd_container('startImage')

        # define camera command(s) help
        self.camera_help = (
            'init_guiders system={0:s} entity={1:s} roispec=<string>'.format(self._system, self._entity),
            'init_image   system={0:s} entity={1:s} deltat=<float>'.format(self._system, self._entity),
            'set_filter   system={0:s} entity={1:s} name=<string>'.format(self._system, self._entity),
            'take_images  system={0:s} entity={1:s} numimages=<int> exptime=<float> shutter=<bool> science=<bool> '
            'guide=<bool> wfs=<bool> imagesequencename=<string>'.format(self._system, self._entity),
            'clear        system={0:s} entity={1:s} nclear=<int>'.format(self._system, self._entity),
            'discard_rows system={0:s} entity={1:s} nrows=<int>'.format(self._system, self._entity),
            'end_image    system={0:s} entity={1:s}'.format(self._system, self._entity),
            'start_image  system={0:s} entity={1:s} shutter=<string> science=<boolean> guide=<boolean> wfs=<boolean> '
            'imagename=<string>'.format(self._system, self._entity)
            )

    # +
    # method: init_guiders()
    # -
    def init_guiders(self, roispec='', timeout=OCS_CAMERA_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.init_guiders() enter, roispec={1:s}, timeout={2:s}'.format(
            self._entity_lc, str(roispec), str(timeout)))

        # check input(s)
        if not isinstance(roispec, str) or roispec == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOROI, 'roispec={0:s}'.format(roispec))
        else:
            self._roispec = roispec

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.init_guiders(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__initGuidersC:
                self._cname = '{0:s}_command_initGuiders'.format(self._entity_lc)
                self._ename = '{0:s}_command_initGuiders roispec={1:s} timeout={2:d}'.format(
                    self._entity_lc, self._roispec, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_initGuiders'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_initGuidersC(); data.roispec = 'roiData')
                self.__initGuidersC.roiSpec = self._roispec

                # issue command (cf. id = mgr.issueCommand_initGuiders(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__initGuiders_id = self.__mgr.issueCommand_initGuiders(self.__initGuidersC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__initGuiders_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__initGuiders_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_initGuiders(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__initGuiders_retval = self.__mgr.waitForCompletion_initGuiders(
                        self.__initGuiders_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__initGuiders_retval))
                    self._get_cmd_status(self._ename, self.__initGuiders_id, self.__initGuiders_retval)

        # exit message
        self.logger.debug('{0:s}.init_guiders() exit'.format(self._entity_lc))

    # +
    # method: init_image()
    # -
    def init_image(self, deltat=0.0, timeout=OCS_CAMERA_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.init_image() enter, deltat={1:s}, timeout={2:s}'.format(
            self._entity_lc, str(deltat), str(timeout)))

        # check input(s)
        if not isinstance(deltat, float) or deltat < 0.0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOTIM, 'deltat={0:s}'.format(deltat))
        else:
            self._deltat = deltat

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.init_image(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__initImageC:
                self._cname = '{0:s}_command_initImage'.format(self._entity_lc)
                self._ename = '{0:s}_command_initImage deltat={1:f} timeout={2:d}'.format(
                    self._entity_lc, self._deltat, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_initImage'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_initImageC(); data.deltat = 5.0)
                self.__initImageC.deltaT = self._deltat

                # issue command (cf. id = mgr.issueCommand_initImage(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__initImage_id = self.__mgr.issueCommand_initImage(self.__initImageC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__initImage_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__initImage_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_initImage(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__initImage_retval = self.__mgr.waitForCompletion_initImage(self.__initImage_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__initImage_retval))
                    self._get_cmd_status(self._ename, self.__initImage_id, self.__initImage_retval)

        # exit message
        self.logger.debug('{0:s}.init_image() exit'.format(self._entity_lc))

    # +
    # method: set_filter()
    # -
    def set_filter(self, name='', timeout=OCS_CAMERA_FILTER_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.set_filter() enter, name={1:s}, timeout={2:s}'.format(
            self._entity_lc, str(name), str(timeout)))

        # check input(s)
        if not isinstance(name, str) or name == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOFIL, 'name={0:s}'.format(name))
        else:
            self._name = name

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.set_filter(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__setFilterC:
                self._cname = '{0:s}_command_setFilter'.format(self._entity_lc)
                self._ename = '{0:s}_command_setFilter name={1:s} timeout={2:d}'.format(
                    self._entity_lc, self._name, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_setFilter'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_setFilterC(); data.name = 'u')
                self.__setFilterC.name = self._name

                # issue command (cf. id = mgr.issueCommand_setFilter(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__setFilter_id = self.__mgr.issueCommand_setFilter(self.__setFilterC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__setFilter_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued', CommandSource=self._instance_name,
                        SequenceNumber=int(self.__setFilter_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_setFilter(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__setFilter_retval = self.__mgr.waitForCompletion_setFilter(
                        self.__setFilter_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__setFilter_retval))
                    self._get_cmd_status(self._ename, self.__setFilter_id, self.__setFilter_retval)

        # exit message
        self.logger.debug('{0:s}.set_filter() exit'.format(self._entity_lc))

    # +
    # method: take_images()
    # -
    def take_images(self, numimages=-1, exptime=-1.0, shutter=False, science=False, guide=False, wfs=False,
                    imagesequencename='',  timeout=OCS_CAMERA_IMAGE_COMMAND_TIMEOUT):

        # entry message
        msg = '{0:s}.take_images() enter, numimages={1:s}'.format(self._entity_lc, str(numimages))
        msg += ' exptime={0:s}'.format(str(exptime))
        msg += ' shutter={0:s}'.format(str(shutter))
        msg += ' science={0:s}'.format(str(science))
        msg += ' guide={0:s}'.format(str(guide))
        msg += ' wfs={0:s}'.format(str(wfs))
        msg += ' imagesequencename={0:s}'.format(str(imagesequencename))
        msg += ' timeout={0:s}'.format(str(timeout))
        self.logger.debug(msg)

        # check input(s)
        if not isinstance(numimages, int) or numimages < 0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOIMG, 'numimages={0:s}'.format(str(numimages)))
        else:
            self._numimages = numimages

        if not isinstance(exptime, float) or exptime < 0.0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOEXP, 'exptime={0:s}'.format(str(exptime)))
        else:
            self._exptime = exptime

        if not isinstance(shutter, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSHT, 'shutter={0:s}'.format(str(shutter)))
        else:
            self._shutter = shutter

        if not isinstance(science, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSCI, 'science={0:s}'.format(str(science)))
        else:
            self._science = science

        if not isinstance(guide, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOGDR, 'guide={0:s}'.format(str(guide)))
        else:
            self._guide = guide

        if not isinstance(wfs, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOWFS, 'wfs={0:s}'.format(str(wfs)))
        else:
            self._wfs = wfs

        if not isinstance(imagesequencename, str) or imagesequencename == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NONAM, 'imagesequencename={0:s}'.format(
                imagesequencename))
        else:
            self._imagesequencename = imagesequencename

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout
            if self._timeout <= self._exptime*2:
                self._timeout = self._exptime * 2 + OCS_CAMERA_COMMAND_TIMEOUT

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.take_images(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__takeImagesC:
                self._cname = '{0:s}_command_takeImages'.format(self._entity_lc)
                self._ename = '{0:s}_command_takeImages() numimages={1:s}'.format(self._entity_lc, str(self._numimages))
                self._ename += ' exptime={0:s}'.format(str(self._exptime))
                self._ename += ' shutter={0:s}'.format(str(self._shutter))
                self._ename += ' science={0:s}'.format(str(self.science))
                self._ename += ' guide={0:s}'.format(str(self._guide))
                self._ename += ' wfs={0:s}'.format(str(self._wfs))
                self._ename += ' imagesequencename={0:s}'.format(self._imagesequencename)
                self._ename += ' timeout={0:s}'.format(str(self._timeout))

                # set up command (cf. mgr.salCommand('camera_command_takeImages'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_takeImagesC(); data.numImages = 2 etc)
                self.__takeImagesC.numImages = self._numimages
                self.__takeImagesC.expTime = self._exptime
                self.__takeImagesC.shutter = self._shutter
                self.__takeImagesC.science = self._science
                self.__takeImagesC.guide = self._guide
                self.__takeImagesC.wfs = self._wfs
                self.__takeImagesC.imageSequenceName = self._imagesequencename

                # issue command (cf. id = mgr.issueCommand_takeImages(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__takeImages_id = self.__mgr.issueCommand_takeImages(self.__takeImagesC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__takeImages_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__takeImages_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_takeImages(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__takeImages_retval = self.__mgr.waitForCompletion_takeImages(
                        self.__takeImages_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__takeImages_retval))
                    self._get_cmd_status(self._ename, self.__takeImages_id, self.__takeImages_retval)

        # exit message
        self.logger.debug('{0:s}.take_images() exit'.format(self._entity_lc))

    # +
    # method: clear()
    # -
    def clear(self, nclear=0, timeout=OCS_CAMERA_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.clear() enter, nclear={1:s}, timeout={2:s}'.format(
            self._entity_lc, str(nclear), str(timeout)))

        # check input(s)
        if not isinstance(nclear, int) or nclear <= 0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOCLR, 'nclear={0:s}'.format(nclear))
        else:
            self._nclear = nclear

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.clear(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__clearC:
                self._cname = '{0:s}_command_initGuiders'.format(self._entity_lc)
                self._ename = '{0:s}_command_initGuiders nclear={1:s} timeout={2:d}'.format(
                    self._entity_lc, self._nclear, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_initGuiders'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_initGuidersC(); data.nclear = 12)
                self.__clearC.nClear = self._nclear

                # issue command (cf. id = mgr.issueCommand_initGuiders(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__clear_id = self.__mgr.issueCommand_clear(self.__clearC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__clear_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__clear_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_initGuiders(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__clear_retval = self.__mgr.waitForCompletion_clear(
                        self.__clear_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__clear_retval))
                    self._get_cmd_status(self._ename, self.__clear_id, self.__clear_retval)

        # exit message
        self.logger.debug('{0:s}.clear() exit'.format(self._entity_lc))

    # +
    # method: discard_rows()
    # -
    def discard_rows(self, nrows=0, timeout=OCS_CAMERA_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.rows() enter, nrows={1:s}, timeout={2:s}'.format(
            self._entity_lc, str(nrows), str(timeout)))

        # check input(s)
        if not isinstance(nrows, int) or nrows <= 0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOROW, 'nrows={0:s}'.format(nrows))
        else:
            self._nrows = nrows

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.discard_rows(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__discardRowsC:
                self._cname = '{0:s}_command_initGuiders'.format(self._entity_lc)
                self._ename = '{0:s}_command_initGuiders nrows={1:s} timeout={2:d}'.format(
                    self._entity_lc, self._nrows, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_initGuiders'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_initGuidersC(); data.nrows = 12)
                self.__discardRowsC.nRows = self._nrows

                # issue command (cf. id = mgr.issueCommand_initGuiders(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__discardRows_id = self.__mgr.issueCommand_discardRows(self.__discardRowsC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__discardRows_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__discardRows_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_initGuiders(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__discardRows_retval = self.__mgr.waitForCompletion_discardRows(
                        self.__discardRows_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__discardRows_retval))
                    self._get_cmd_status(self._ename, self.__discardRows_id, self.__discardRows_retval)

        # exit message
        self.logger.debug('{0:s}.discard_rows() exit'.format(self._entity_lc))

    # +
    # method: end_image()
    # -
    def end_image(self, timeout=OCS_CAMERA_COMMAND_TIMEOUT):

        # entry message
        self.logger.debug('{0:s}.end_image() enter, timeout={1:s}'.format(
            self._entity_lc, str(timeout)))

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.end_image(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__endImageC:
                self._cname = '{0:s}_command_initGuiders'.format(self._entity_lc)
                self._ename = '{0:s}_command_initGuiders timeout={1:d}'.format(
                    self._entity_lc, self._timeout)

                # set up command (cf. mgr.salCommand('camera_command_initGuiders'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_initGuidersC(); data.state = 12)
                self.__endImageC.state = os.getpid()

                # issue command (cf. id = mgr.issueCommand_initGuiders(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__endImage_id = self.__mgr.issueCommand_endImage(self.__endImageC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__endImage_id))

                # issue an ocsCommandIssued event
                if self._instance_evp:
                    self._ocsid = ocs_id(False)
                    self._instance_evp.send_event(
                        'ocsCommandIssued',
                        CommandSource=self._instance_name,
                        SequenceNumber=int(self.__endImage_id),
                        Identifier=float(self._ocsid),
                        Timestamp=ocs_mjd_to_iso(self._ocsid),
                        CommandSent=self._ename,
                        ReturnValue=int(SAL__CMD_ACK),
                        priority=SAL__EVENT_INFO)

                # wait for command (cf. retval = mgr.waitForCompletion_initGuiders(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__endImage_retval = self.__mgr.waitForCompletion_endImage(
                        self.__endImage_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__endImage_retval))
                    self._get_cmd_status(self._ename, self.__endImage_id, self.__endImage_retval)

        # exit message
        self.logger.debug('{0:s}.end_image() exit'.format(self._entity_lc))

    # +
    # method: start_image()
    # -
    def start_image(self, shutter=False, science=False, guide=False, wfs=False,
                    imagename='',  timeout=OCS_CAMERA_IMAGE_COMMAND_TIMEOUT):

        # entry message
        msg = '{0:s}.start_image() enter,'.format(self._entity_lc)
        msg += ' shutter={0:s}'.format(str(shutter))
        msg += ' science={0:s}'.format(str(science))
        msg += ' guide={0:s}'.format(str(guide))
        msg += ' wfs={0:s}'.format(str(wfs))
        msg += ' imagename={0:s}'.format(str(imagename))
        msg += ' timeout={0:s}'.format(str(timeout))
        self.logger.debug(msg)

        if not isinstance(shutter, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSHT, 'shutter={0:s}'.format(str(shutter)))
        else:
            self._shutter = shutter

        if not isinstance(science, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSCI, 'science={0:s}'.format(str(science)))
        else:
            self._science = science

        if not isinstance(guide, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOGDR, 'guide={0:s}'.format(str(guide)))
        else:
            self._guide = guide

        if not isinstance(wfs, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOWFS, 'wfs={0:s}'.format(str(wfs)))
        else:
            self._wfs = wfs

        if not isinstance(imagename, str) or imagename == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NONAM, 'imagename={0:s}'.format(
                imagename))
        else:
            self._imagename = imagename

        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, 'timeout={0:s}'.format(str(timeout)))
        else:
            self._timeout = timeout
            if self._timeout <= self._exptime*2:
                self._timeout = self._exptime * 2 + OCS_CAMERA_COMMAND_TIMEOUT

        # in simulation, sleep for a random time
        if self._simulate:
            stime = random.uniform(0, 5)
            self.logger.info('{0:s}.start_image(), in simulation with sleep={1:s}'.format(self._entity_lc, str(stime)))
            time.sleep(stime)

        # send command
        else:
            if self.__mgr and self.__startImageC:
                self._cname = '{0:s}_command_startImage'.format(self._entity_lc)
                self._ename = '{0:s}_command_startImage()'.format(self._entity_lc)
                self._ename += ' shutter={0:s}'.format(str(self._shutter))
                self._ename += ' science={0:s}'.format(str(self.science))
                self._ename += ' guide={0:s}'.format(str(self._guide))
                self._ename += ' wfs={0:s}'.format(str(self._wfs))
                self._ename += ' imagesequencename={0:s}'.format(self._imagesequencename)
                self._ename += ' timeout={0:s}'.format(str(self._timeout))

                # set up command (cf. mgr.salCommand('camera_command_startImage'))
                self.logger.debug('setting up for command {0:s}'.format(self._ename))
                self.__mgr.salCommand(self._cname)

                # set up payload (cf. data = camera_command_startImageC(); data.numImages = 2 etc)
                self.__startImageC.shutter = self._shutter
                self.__startImageC.science = self._science
                self.__startImageC.guide = self._guide
                self.__startImageC.wfs = self._wfs
                self.__startImageC.imageName = self._imagename

                # issue command (cf. id = mgr.issueCommand_startImage(data))
                self.logger.debug('issuing command {0:s}'.format(self._ename))
                self.__startImage_id = self.__mgr.issueCommand_startImage(self.__startImageC)
                self.logger.debug('issued command {0:s}, id={1:d}'.format(self._ename, self.__startImage_id))

                # wait for command (cf. retval = mgr.waitForCompletion_startImage(id, timeout))
                if self._timeout > 0:
                    self.logger.debug('waiting for command {0:s} to complete'.format(self._ename))
                    self.__startImage_retval = self.__mgr.waitForCompletion_startImage(
                        self.__startImage_id, self._timeout)
                    self.logger.debug('waited for command {0:s} to complete, retval={1:d}'.format(
                        self._ename, self.__startImage_retval))
                    self._get_cmd_status(self._ename, self.__startImage_id, self.__startImage_retval)

        # exit message
        self.logger.debug('{0:s}.start_image() exit'.format(self._entity_lc))

    # +
    # decorator(s)
    # -
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=''):
        self.logger.critical('name cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'name={0:s} cannot be set'.format(str(name)))

    @property
    def roispec(self):
        return self._roispec

    @roispec.setter
    def roispec(self, roispec=''):
        self.logger.critical('roispec cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'roispec={0:s} cannot be set'.format(str(roispec)))

    @property
    def deltat(self):
        return self._deltat

    @deltat.setter
    def deltat(self, deltat=0.0):
        self.logger.critical('deltat cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'deltat={0:s} cannot be set'.format(str(deltat)))

    @property
    def nclear(self):
        return self._nclear

    @nclear.setter
    def nclear(self, nclear=0):
        self.logger.critical('nclear cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'nclear={0:s} cannot be set'.format(str(nclear)))

    @property
    def nrows(self):
        return self._nrows

    @nrows.setter
    def nrows(self, nrows=0):
        self.logger.critical('nrows cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'nrows={0:s} cannot be set'.format(str(nrows)))

    @property
    def numimages(self):
        return self._numimages

    @numimages.setter
    def numimages(self, numimages=0):
        self.logger.critical('numimages cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'numimages={0:s} cannot be set'.format(str(numimages)))

    @property
    def exptime(self):
        return self._exptime

    @exptime.setter
    def exptime(self, exptime=0.0):
        self.logger.critical('exptime cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'exptime={0:s} cannot be set'.format(str(exptime)))

    @property
    def shutter(self):
        return self._shutter

    @shutter.setter
    def shutter(self, shutter=False):
        self.logger.critical('shutter cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'shutter={0:s} cannot be set'.format(str(shutter)))

    @property
    def science(self):
        return self._science

    @science.setter
    def science(self, science=False):
        self.logger.critical('science cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'science={0:s} cannot be set'.format(str(science)))

    @property
    def guide(self):
        return self._guide

    @guide.setter
    def guide(self, guide=False):
        self.logger.critical('guide cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'guide={0:s} cannot be set'.format(str(guide)))

    @property
    def wfs(self):
        return self._wfs

    @wfs.setter
    def wfs(self, wfs=False):
        self.logger.critical('wfs cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'wfs={0:s} cannot be set'.format(str(wfs)))

    @property
    def imagename(self):
        return self._imagename

    @imagename.setter
    def imagename(self, imagename=''):
        self.logger.critical('imagename cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'imagename={0:s} cannot be set'.format(str(imagename)))

    @property
    def imagesequencename(self):
        return self._imagesequencename

    @imagesequencename.setter
    def imagesequencename(self, imagesequencename=''):
        self.logger.critical('imagesequencename cannot be reset by this method!')
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS,
                                        'imagesequencename={0:s} cannot be set'.format(str(imagesequencename)))

# +
# main()
# -
if __name__ == '__main__':

    camera = None
    try:
        camera = OcsCameraEntity('CCS', 'Camera', False)
    except OcsCameraEntityException as e:
        print(e.errstr)

    if camera:

        # get logger
        camlog = camera.logger
        camlog.info('{0:s}'.format(camera.__str__()))

        # start of night
        camlog.info('camera.entercontrol()')
        camera.entercontrol()

        camlog.info('camera.start(\'Normal\')')
        camera.start('Normal')

        camlog.info('camera.enable()')
        camera.enable()

        # do some behavioural commands
        camlog.info('camera.set_filter(\'g-9\', 60)')
        camera.set_filter('g-9', 60)

        camlog.info('camera.init_image(4.0)')
        camera.init_image(4.0)

        camlog.info('camera take_images(2, 15.0, True, True, True, False, \'pndTest\', 40)')
        camera.take_images(2, 15.0, True, True, True, False, 'pndTest', 40)

        # this currently fails because of a lack of support in the ToyOCSBridge?
        camlog.info('camera.init_guiders(\'1,1,1,1 100,100,100,100 32,32,32,32\', OCS_CAMERA_COMMAND_TIMEOUT)')
        camera.init_guiders('1,1,1,1 100,100,100,100 32,32,32,32', OCS_CAMERA_COMMAND_TIMEOUT)

        # end of night
        camlog.info('camera.disable()')
        camera.disable()

        camlog.info('camera.standby()')
        camera.standby()

        camlog.info('camera.exitcontrol()')
        camera.exitcontrol()

        # execute destructor
        camlog.info('del camera')
        del camera
