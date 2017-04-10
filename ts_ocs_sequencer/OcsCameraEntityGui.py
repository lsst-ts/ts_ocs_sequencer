#!/usr/bin/env python


# +
# imports
# -
from OcsGenericEntityGui import *
from OcsCameraEntity import *


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsCameraEntityGui.py, contains the code for the (temporary)
TkInter GUI for the camera commandable entity. There are no Python (unit) tests (as yet).

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.


Example:

    root = Tk()
    try:
        x = OcsCameraEntityGui(parent=root, system='CCS', entity='Camera', Standalone=True)
    except OcsCameraEntityError as e:
        print(e.errstr)
    if x:
        root.mainloop()

API:

    OcsCameraEntityGui(parent=None, system='CCS', entity='Camera', Standalone=True)
        class initializes the CCS sub-system and Camera entity within the parent frame. If Standalone is True,
        a Quit button is provided. If Standalone is False, no Quit button is created and the object is
        suitable for embedded within other frames (see $TS_OCS_SEQEUNCER_SRC/OcsConsoleGui.py).

CLI:

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
__file__ = "OcsCameraEntityGui.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsCameraEntityGui() inherits from OcsGenericEntityGui
# -
class OcsCameraEntityGui(OcsGenericEntityGui):

    # +
    # __init__ method
    # -
    def __init__(self, parent=None, system='CCS', entity='Camera', standalone=True):

        # get arguments
        self._parent = parent
        self._system = system
        self._entity = entity
        self._standalone = standalone

        # declare some variables and initialize them
        self._deltat = None
        self._name = None
        self._nrows = None
        self._nclear = None
        self._result = None
        self._roispec = None
        self._numimages = None
        self._exptime = None
        self._shutter = None
        self._science = None
        self._guide = None
        self._wfs = None
        self._imagesequencename = None
        self._imagename = None

        # create an instance of this generic entity
        self._camera = OcsCameraEntity(self._system, self._entity, True)

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=ocsGenericEntityBackgroundColour.get(
            self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
        self._generic = OcsGenericEntityGui(self._parent, self._system, self._entity, self._standalone)
        Label(self._parent, text='{0:s} {1:s}'.format(self._system, self._entity), foreground='blue', bg=ocsGenericEntityBackgroundColour.get(
            self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), font=('helvetica', 12, 'normal')).grid(
            row=0, sticky=NSEW)
        #Label(self._parent, text=self._entity, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(
        #    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
        #    font=('helvetica', 12, 'bold')).grid(row=1, sticky=NSEW)
        self.create_camera_buttons(self._parent, self._system)

        self._generic._simFlag.trace('w', self.this_change)

    # +
    # (override trace) method(s)
    # -
    def this_change(self, *args):
        self._camera.logger.debug("args = {0:s}".format(str(args)))
        # self._camera.logger.debug("self._camera._simulate = {0:d}".format(self._camera._simulate))
        # self._camera.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        simflag = self._generic._simFlag.get()
        self._camera._simulate = simflag
        self._generic._this._simulate = simflag
        # self._camera.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        # self._camera.logger.debug("self._camera._simulate = {0:d}".format(self._camera._simulate))

    # +
    # methods()
    # -
    def get_camera_command_dialog_string(self, name=''):
        s = 'camera command dialog box'
        for el in self._camera.camera_help:
            t = el.split()
            if t[0].lower() == name.lower():
                return el
        return s

    # +
    # (command) methods()
    # -
    def init_guiders_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('initGuiders'), ['roiSpec'])
        if self._camera:
            if self._result:
                self._roispec = self._result['roiSpec']
                self._camera.logger.debug("calling self._camera.init_guiders('{0:s}')".format(str(self._roispec)))
                self._camera.init_guiders(roispec=self._roispec)
            else:
                self._roispec = ''
                self._camera.logger.debug("self._camera.init_guiders('{0:s}') cancelled".format(str(self._roispec)))

    def init_image_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('initImage'), ['deltaT'])
        if self._camera:
            if self._result:
                self._deltat = self._result['deltaT']
                self._camera.logger.debug("calling self._camera.init_image({0:s})".format(str(self._deltat)))
                self._camera.init_image(deltat=float(self._deltat))
            else:
                self._deltat = ''
                self._camera.logger.debug("self._camera.init_image({0:s}) cancelled".format(str(self._deltat)))

    def set_filter_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('setFilter'), ['Name'])
        if self._camera:
            if self._result:
                self._name = self._result['Name']
                self._camera.logger.debug("calling self._camera.set_filter('{0:s}')".format(str(self._name)))
                self._camera.set_filter(name=self._name)
            else:
                self._name = ''
                self._camera.logger.debug("self._camera.set_filter('{0:s}') cancelled".format(str(self._name)))

    def take_images_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('takeImages'),
                       ['numImages', 'expTime', 'shutterState', 'scienceActive',
                        'guidersActive', 'wfsActive', 'imageName'])
        if self._camera:
            if self._result:
                self._numimages = self._result['numImages']
                self._exptime = self._result['expTime']
                self._shutter = ocsGenericEntityLogicDictionary.get(self._result['shutterState'].lower(), False)
                self._science = ocsGenericEntityLogicDictionary.get(self._result['scienceActive'].lower(), False)
                self._guide = ocsGenericEntityLogicDictionary.get(self._result['guidersActive'].lower(), False)
                self._wfs = ocsGenericEntityLogicDictionary.get(self._result['wfsActive'].lower(), False)
                self._imagesequencename = self._result['imageName']
                self._camera.logger.debug("calling self._camera.take_images({0:d}, {1:.2f}, {2:s}, {3:s}, "
                                          "{4:s}, {5:s}, '{6:s}')".format(int(self._numimages),
                                                                          float(self._exptime), str(self._shutter),
                                                                          str(self._science), str(self._guide),
                                                                          str(self._wfs), self._imagesequencename))
                self._camera.take_images(numimages=int(self._numimages), exptime=float(self._exptime),
                                         shutter=self._shutter, science=self._science, guide=self._guide,
                                         wfs=self._wfs, imagesequencename=self._imagesequencename)
            else:
                self._numimages = '0'
                self._exptime = '0.0'
                self._shutter = False
                self._science = False
                self._guide = False
                self._wfs = False
                self._imagesequencename = ''
                self._camera.logger.debug("self._camera.take_images({0:d}, {1:.2f}, {2:s}, {3:s}, {4:s}, "
                                          "{5:s}, '{6:s}') cancelled".format(int(self._numimages),
                                                                             float(self._exptime), str(self._shutter),
                                                                             str(self._science), str(self._guide),
                                                                             str(self._wfs), self._imagesequencename))

    def clear_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('clear'), ['nClear'])
        if self._camera:
            if self._result:
                self._nclear = self._result['nClear']
                self._camera.logger.debug("calling self._camera.clear('{0:s}')".format(str(self._nclear)))
                self._camera.clear(nclear=int(self._nclear))
            else:
                self._nclear = ''
                self._camera.logger.debug("self._camera.clear('{0:s}') cancelled".format(str(self._nclear)))

    def discard_rows_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('discardRows'), ['nRows'])
        if self._camera:
            if self._result:
                self._nrows = self._result['nRows']
                self._camera.logger.debug("calling self._camera.discard_rows('{0:s}')".format(str(self._nrows)))
                self._camera.discard_rows(nrows=int(self._nrows))
            else:
                self._nrows = ''
                self._camera.logger.debug("self._camera.discard_rows('{0:s}') cancelled".format(str(self._nrows)))

    def end_image_handler(self):
        if self._camera:
            if self._result:
                self._camera.end_image()

    def start_image_handler(self):
        OcsEntryDialog(self, self.get_camera_command_dialog_string('startImage'),
                       ['shutterState', 'scienceActive', 'guidersActive', 'wfsActive', 'imageName'])
        if self._camera:
            if self._result:
                self._shutter = ocsGenericEntityLogicDictionary.get(self._result['shutterState'].lower(), False)
                self._science = ocsGenericEntityLogicDictionary.get(self._result['scienceActive'].lower(), False)
                self._guide = ocsGenericEntityLogicDictionary.get(self._result['guidersActive'].lower(), False)
                self._wfs = ocsGenericEntityLogicDictionary.get(self._result['wfsActive'].lower(), False)
                self._imagename = self._result['imageName']
                self._camera.logger.debug("calling self._camera.start_image({0:s}, {1:s}, {2:s}, {3:s}, "
                                          "'{4:s}')".format(str(self._shutter), str(self._science),
                                                            str(self._guide), str(self._wfs), str(self._imagename)))
                self._camera.start_image(shutter=self._shutter, science=self._science, guide=self._guide,
                                         wfs=self._wfs, imagename=self._imagename)
            else:
                self._shutter = False
                self._science = False
                self._guide = False
                self._wfs = False
                self._imagename = ''
                self._camera.logger.debug("self._camera.startImage({0:s}, {1:s}, {2:s}, {3:s}, "
                                          "'{4:s}') cancelled".format(str(self._shutter), str(self._science),
                                                                      str(self._guide), str(self._wfs),
                                                                      str(self._imagename)))

    # +
    # createCameraButtons() method
    # -
    def create_camera_buttons(self, _parent=None, system=''):
        self._parent = _parent
        self._system = system
        for eh in self._camera.camera_help:
            t = eh.split()
            tl = t[0].lower()
            if tl == 'init_guiders':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.init_guiders_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=15, sticky=NSEW)
            elif tl == 'init_image':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.init_image_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=16, sticky=NSEW)
            elif tl == 'set_filter':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.set_filter_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=17, sticky=NSEW)
            elif tl == 'take_images':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.take_images_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=18, sticky=NSEW)
            elif tl == 'clear':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.clear_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=19, sticky=NSEW)
            elif tl == 'discard_rows':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.discard_rows_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=20, sticky=NSEW)
            elif tl == 'end_image':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.end_image_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=21, sticky=NSEW)
            elif tl == 'start_image':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                                command=self.start_image_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=22, sticky=NSEW)
            else:
                pass


# +
# main()
# -
if __name__ == '__main__':
    root = Tk()
    x = OcsCameraEntityGui(root, 'CCS', 'Camera', True)
    if x:
        root.mainloop()
