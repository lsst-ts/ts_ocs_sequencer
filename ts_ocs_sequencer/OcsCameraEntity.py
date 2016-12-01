#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsGenericEntity import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Camera entity class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsCameraEntity.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsCameraEntity()
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
        self._system = 'CCS'
        self._system_lc = self._system.lower()
        self._entity = 'Camera'
        self._entity_lc = self._entity.lower()
        self._simulate = simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # initialize the superclass
        super(OcsCameraEntity, self).__init__(self._system, self._entity, self._simulate)

        # declare some variables and initialize them
        self.logger.debug("Initializing variables")
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

        # method agument value(s)
        self._roiSpec = None
        self._deltaT = None
        self._name = None
        self._numImages = None
        self._expTime = None
        self._shutter = None
        self._science = None
        self._guide = None
        self._wfs = None
        self._imafgeSequenceName = None
        self._timeout = OCS_CAMERA_COMMAND_TIMEOUT

        # import the SAL (cf. from SALPY_camera import *)
        mname = 'SALPY_{0:s}'.format(self._entity_lc)
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal = ocs_sal_import(mname)
        if self.__sal:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # get mgr object (cf. mgr = SAL_camera())
        aname = 'SAL_{0:s}'.format(self._entity_lc)
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal, aname)
        if mgr:
            self.__mgr = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # initGuiders data structure (cf. data = camera_command_initGuidersC())
        self.__initGuidersC = self._get_sal_cmdC('initGuiders')

        # initImage data structure (cf. data = camera_command_initImageC())
        self.__initImageC = self._get_sal_cmdC('initImage')

        # setFilter data structure (cf. data = camera_command_setFilterC())
        self.__setFilterC = self._get_sal_cmdC('setFilter')

        # takeImages data structure (cf. data = camera_command_takeImagesC())
        self.__takeImagesC = self._get_sal_cmdC('takeImages')

        # ToBeEnabled: clear data structure (cf. data = camera_command_clearC())
        # self.__clearC = self._get_sal_cmdC('clear')

        # ToBeEnabled: discardRows data structure (cf. data = camera_command_discardRowsC())
        # self.__discardRowsC = self._get_sal_cmdC('discardRows')

        # ToBeEnabled: endImage data structure (cf. data = camera_command_endImageC())
        # self.__endImageC = self._get_sal_cmdC('endImage')

        # ToBeEnabled: startImage data structure (cf. data = camera_command_startImageC())
        # self.__startImageC = self._get_sal_cmdC('startImage')

        # define camera command(s) help
        self.logger.debug("Camera> Defining help")
        self.camera_help = (
            'initGuiders system={0:s} entity={1:s} roiSpec=<string>'.format(self._system, self._entity),
            'initImage   system={0:s} entity={1:s} deltaT=<float>'.format(self._system, self._entity),
            'setFilter   system={0:s} entity={1:s} name=<string>'.format(self._system, self._entity),
            'takeImages  system={0:s} entity={1:s} numImages=<int> expTime=<float> shutter=<bool> science=<bool> guide=<bool> wfs=<bool> imageSequenceName=<string>'.format(self._system, self._entity),
            'clear       system={0:s} entity={1:s} nClear=<int>'.format(self._system, self._entity),
            'discardRows system={0:s} entity={1:s} rows=<int>'.format(self._system, self._entity),
            'endImage    system={0:s} entity={1:s}'.format(self._system, self._entity),
            'startImage  system={0:s} entity={1:s} shutter=<string> science=<boolean> guide=<boolean> wfs=<boolean> imageName=<string>'.format(self._system, self._entity)
            )
        self.logger.debug("Camera> Defined help ok")

        self.logger.debug("Camera> Started {0:s} {1:s} commandable entity ok".format(self._system, self._entity))


    # +
    # method: initGuiders()
    # -
    def initGuiders(self, roiSpec='', timeout=OCS_CAMERA_COMMAND_TIMEOUT):
        self.logger.debug("initGuiders() enter, roiSpec={0:s}, timeout={1:s}".format(str(roiSpec), str(timeout)))
        # check input(s)
        if not isinstance(roiSpec, str) or roiSpec == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOROI, "roiSpec={0:s}".format(roiSpec))
        else:
            self._roiSpec = roiSpec
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVAL, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout
        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("initGuiders(), in simulation with sleep={0:s}".format(str(stime)))
        else:
            if self.__mgr and self.__initGuidersC:
                cname = '{0:s}_command_initGuiders'.format(self._entity_lc)
                # set up command (cf. mgr.salCommand("camera_command_initGuiders"))
                self.logger.debug("setting up for command {0:s}".format(cname))
                self.__mgr.salCommand(cname)
                # set up payload (cf. data = camera_command_initGuidersC(); data.roiSpec = 'roiData')
                self.__initGuidersC.roiSpec = self._roiSpec
                # issue command (cf. id = mgr.issueCommand_initGuiders(data))
                self.logger.debug("issuing command {0:s}".format(cname))
                self.__initGuiders_id = self.__mgr.issueCommand_initGuiders(self.__initGuidersC)
                self.logger.debug("issued command {0:s}, id={1:d}".format(cname,self.__initGuiders_id))
                if self._timeout > 0:
                    # wait for command (cf. retval = mgr.waitForCompletion_initGuiders(id, timeout))
                    self.logger.debug("waiting for command {0:s} to complete".format(cname))
                    self.__initGuiders_retval = self.__mgr.waitForCompletion_initGuiders(self.__initGuiders_id, self._timeout)
                    self.logger.debug("waited for command {0:s} to complete, retval={1:d}".format(cname,self.__initGuiders_retval))
                    self._get_cmd_status(cname, self.__initGuiders_retval)
        self.logger.debug("initGuiders() exit")


    # +
    # method: initImage()
    # -
    def initImage(self, deltaT=0.0, timeout=OCS_CAMERA_COMMAND_TIMEOUT):
        self.logger.debug("initImage() enter, deltaT={0:s}, timeout={1:s}".format(str(deltaT), str(timeout)))
        # check input(s)
        if not isinstance(deltaT, float) or deltaT < 0.0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOTIM, "deltaT={0:s}".format(deltaT))
        else:
            self._deltaT = deltaT
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVAL, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout
        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("initImage(), in simulation with sleep={0:s}".format(str(stime)))
        else:
            if self.__mgr and self.__initImageC:
                cname = '{0:s}_command_initImage'.format(self._entity_lc)
                # set up command (cf. mgr.salCommand("camera_command_initImage"))
                self.logger.debug("setting up for command {0:s}".format(cname))
                self.__mgr.salCommand(cname)
                # set up payload (cf. data = camera_command_initImageC(); data.deltaT = 5.0)
                self.__initImageC.deltaT = self._deltaT
                # issue command (cf. id = mgr.issueCommand_initImage(data))
                self.logger.debug("issuing command {0:s}".format(cname))
                self.__initImage_id = self.__mgr.issueCommand_initImage(self.__initImageC)
                self.logger.debug("issued command {0:s}, id={1:d}".format(cname,self.__initImage_id))
                if self._timeout > 0:
                    # wait for command (cf. retval = mgr.waitForCompletion_initImage(id, timeout))
                    self.logger.debug("waiting for command {0:s} to complete".format(cname))
                    self.__initImage_retval = self.__mgr.waitForCompletion_initImage(self.__initImage_id, self._timeout)
                    self.logger.debug("waited for command {0:s} to complete, retval={1:d}".format(cname,self.__initImage_retval))
                    self._get_cmd_status(cname, self.__initImage_retval)
        self.logger.debug("initImage() exit")


    # +
    # method: setFilter()
    # -
    def setFilter(self, name='', timeout=OCS_CAMERA_COMMAND_TIMEOUT):
        self.logger.debug("setFilter() enter, name={0:s}, timeout={1:s}".format(str(name), str(timeout)))
        # check input(s)
        if not isinstance(name, str) or name == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOFIL, "name={0:s}".format(name))
        else:
            self._name = name
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVAL, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout
        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("setFilter(), in simulation with sleep={0:s}".format(str(stime)))
        else:
            if self.__mgr and self.__setFilterC:
                cname = '{0:s}_command_setFilter'.format(self._entity_lc)
                # set up command (cf. mgr.salCommand("camera_command_setFilter"))
                self.logger.debug("setting up for command {0:s}".format(cname))
                self.__mgr.salCommand(cname)
                # set up payload (cf. data = camera_command_setFilterC(); data.name = 'u')
                self.__setFilterC.name = self._name
                # issue command (cf. id = mgr.issueCommand_setFilter(data))
                self.logger.debug("issuing command {0:s}".format(cname))
                self.__setFilter_id = self.__mgr.issueCommand_setFilter(self.__setFilterC)
                self.logger.debug("issued command {0:s}, id={1:d}".format(cname,self.__setFilter_id))
                if self._timeout > 0:
                    # wait for command (cf. retval = mgr.waitForCompletion_setFilter(id, timeout))
                    self.logger.debug("waiting for command {0:s} to complete".format(cname))
                    self.__setFilter_retval = self.__mgr.waitForCompletion_setFilter(self.__setFilter_id, self._timeout)
                    self.logger.debug("waited for command {0:s} to complete, retval={1:d}".format(cname,self.__setFilter_retval))
                    self._get_cmd_status(cname, self.__setFilter_retval)
        self.logger.debug("setFilter() exit")


    # +
    # method: takeImages()
    # -
    def takeImages(self, numImages=-1, expTime=-1.0, shutter=False, science=False, guide=False, wfs=False, imageSequenceName='',  timeout=OCS_CAMERA_COMMAND_TIMEOUT):
        self.logger.debug("takeImages() enter, numImages={0:s}, expTime={1:s}, shutter={2:s}, science={3:s}, guide={4:s}, wfs={5:s}, imageSequenceName={6:s}, timeout={7:s}".format(str(numImages), str(expTime), str(shutter), str(science), str(guide), str(wfs), str(imageSequenceName), str(timeout)))
        # check input(s)
        if not isinstance(numImages, int) or numImages < 0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOIMG, "numImages={0:s}".format(str(numImages)))
        else:
            self._numImages = numImages
        if not isinstance(expTime, float) or expTime < 0.0:
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOEXP, "expTime={0:s}".format(str(expTime)))
        else:
            self._expTime = expTime
        if not isinstance(shutter, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSHT, "shutter={0:s}".format(str(shutter)))
        else:
            self._shutter = shutter
        if not isinstance(science, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSCI, "science={0:s}".format(str(science)))
        else:
            self._science = science
        if not isinstance(guide, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOGDR, "guide={0:s}".format(str(guide)))
        else:
            self._guide = guide
        if not isinstance(wfs, bool):
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOWFS, "wfs={0:s}".format(str(wfs)))
        else:
            self._wfs = wfs
        if not isinstance(imageSequenceName, str) or imageSequenceName == '':
            raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NONAM, "imageSequenceName={0:s}".format(imageSequenceName))
        else:
            self._imageSequenceName = imageSequenceName
        if not isinstance(timeout, int) or timeout < 0:
            raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVAL, "timeout={0:s}".format(str(timeout)))
        else:
            self._timeout = timeout
            if self._timeout <= self._expTime*2:
                self._timeout = self._expTime * 2 + OCS_CAMERA_COMMAND_TIMEOUT
        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("takeImages(), in simulation with sleep={0:s}".format(str(stime)))
        else:
            if self.__mgr and self.__takeImagesC:
                cname = '{0:s}_command_takeImages'.format(self._entity_lc)
                # set up command (cf. mgr.salCommand("camera_command_takeImages"))
                self.logger.debug("setting up for command {0:s}".format(cname))
                self.__mgr.salCommand(cname)
                # set up payload (cf. data = camera_command_takeImagesC(); data.numImages = 2 etc)
                self.__takeImagesC.numImages = self._numImages
                self.__takeImagesC.expTime = self._expTime
                self.__takeImagesC.shutter = self._shutter
                self.__takeImagesC.science = self._science
                self.__takeImagesC.guide = self._guide
                self.__takeImagesC.wfs = self._wfs
                self.__takeImagesC.imageSequenceName = self._imageSequenceName
                # issue command (cf. id = mgr.issueCommand_takeImages(data))
                self.logger.debug("issuing command {0:s}".format(cname))
                self.__takeImages_id = self.__mgr.issueCommand_takeImages(self.__takeImagesC)
                self.logger.debug("issued command {0:s}, id={1:d}".format(cname,self.__takeImages_id))
                if self._timeout > 0:
                    # wait for command (cf. retval = mgr.waitForCompletion_takeImages(id, timeout))
                    self.logger.debug("waiting for command {0:s} to complete".format(cname))
                    self.__takeImages_retval = self.__mgr.waitForCompletion_takeImages(self.__takeImages_id, self._timeout)
                    self.logger.debug("waited for command {0:s} to complete, retval={1:d}".format(cname,self.__takeImages_retval))
                    self._get_cmd_status(cname, self.__takeImages_retval)
        self.logger.debug("takeImages() exit")


    # +
    # decorator(s)
    # -
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=''):
        self.logger.critical("name cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "name={0:s} cannot be set".format(str(name)))

    @property
    def roiSpec(self):
        return self._roiSpec

    @roiSpec.setter
    def roiSpec(self, roiSpec=''):
        self.logger.critical("roiSpec cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "roiSpec={0:s} cannot be set".format(str(roiSpec)))

    @property
    def deltaT(self):
        return self._deltaT

    @deltaT.setter
    def deltaT(self, deltaT=0.0):
        self.logger.critical("deltaT cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "deltaT={0:s} cannot be set".format(str(deltaT)))

    @property
    def numImages(self):
        return self._numImages

    @numImages.setter
    def numImages(self, numImages=0):
        self.logger.critical("numImages cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "numImages={0:s} cannot be set".format(str(numImages)))

    @property
    def expTime(self):
        return self._expTime

    @expTime.setter
    def expTime(self, expTime=0.0):
        self.logger.critical("expTime cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "expTime={0:s} cannot be set".format(str(expTime)))

    @property
    def shutter(self):
        return self._shutter

    @shutter.setter
    def shutter(self, shutter=False):
        self.logger.critical("shutter cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "shutter={0:s} cannot be set".format(str(shutter)))

    @property
    def science(self):
        return self._science

    @science.setter
    def science(self, science=False):
        self.logger.critical("science cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "science={0:s} cannot be set".format(str(science)))

    @property
    def guide(self):
        return self._guide

    @guide.setter
    def guide(self, guide=False):
        self.logger.critical("guide cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "guide={0:s} cannot be set".format(str(guide)))

    @property
    def wfs(self):
        return self._wfs

    @wfs.setter
    def wfs(self, wfs=False):
        self.logger.critical("wfs cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "wfs={0:s} cannot be set".format(str(wfs)))

    @property
    def imageSequenceName(self):
        return self._imageSequenceName

    @imageSequenceName.setter
    def imageSequenceName(self, imageSequenceName=''):
        self.logger.critical("imageSequenceName cannot be reset by this method!")
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, "imageSequenceName={0:s} cannot be set".format(str(imageSequenceName)))

# +
# main()
# -
if __name__ == "__main__":

    camera = None
    try:
        camera = OcsCameraEntity('CCS', 'Camera', False)
    except OcsCameraEntityException as e:
        print(e.errstr)

    if camera:

        # get logger
        camlog = camera.logger
        camlog.info("{0:s}".format(camera.__str__()))

        # start of night
        camlog.info("camera.entercontrol()")
        camera.entercontrol()

        camlog.info("camera.start(Normal)")
        camera.start('Normal')

        camlog.info("camera.enable()")
        camera.enable()

        # do some behavioural commands
        camlog.debug("camera.filter('i-9', 60)")
        camera.setFilter('i-9', 60)

        camlog.debug("camera.initImage(1.5)")
        camera.initImage(1.5)

        camlog.debug("camera takeImages(2, 15.0, True, True, True, False, 'pndTest', 40)")
        camera.takeImages(2, 15.0, True, True, True, False, "pndTest", 40)

        # this currently fails because of a lack of support in the ToyOCSBridge?
        camlog.debug("camera.initGuiders('1,1,1,1 100,100,100,100 32,32,32,32', OCS_CAMERA_COMMAND_TIMEOUT)")
        camera.initGuiders('1,1,1,1 100,100,100,100 32,32,32,32', OCS_CAMERA_COMMAND_TIMEOUT)

        # end of night
        camlog.info("camera.disable()")
        camera.disable()

        camlog.info("camera.standby()")
        camera.standby()

        camlog.info("camera.exitcontrol()")
        camera.exitcontrol()

