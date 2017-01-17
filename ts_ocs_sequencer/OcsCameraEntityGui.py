#!/usr/bin/env python


#+
# imports
#-
from OcsGenericEntityGui import *
from OcsCameraEntity import *


#+
# class: OcsCameraEntityGui() inherits from OcsGenericEntityGui
#-
class OcsCameraEntityGui(OcsGenericEntityGui):

    #+
    # __init__ method
    #-
    def __init__(self, parent=None, system='CCS', entity='Camera', standalone=True):

        # get arguments
        self._parent = parent
        self._system = system
        self._entity = entity
        self._standalone = standalone

        # create an instance of this generic entity
        self._camera = OcsCameraEntity(self._system, self._entity, True)

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
        self._generic = OcsGenericEntityGui(self._parent, self._system, self._entity, self._standalone)
        Label(self._parent, text=self._system, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'normal')).grid(row=0,sticky=NSEW)
        Label(self._parent, text=self._entity, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'bold')).grid(row=1,sticky=NSEW)
        self.createCameraButtons(self._parent,self._system)

        self._generic._simFlag.trace('w',self.thisChange)

    #+
    # (override trace) method(s)
    #-
    def thisChange(self, *args):
        self._camera.logger.debug("self._camera._simulate = {0:d}".format(self._camera._simulate))
        self._camera.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        self._camera._simulate = self._generic._this._simulate = self._generic._simFlag.get()
        self._camera.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        self._camera.logger.debug("self._camera._simulate = {0:d}".format(self._camera._simulate))

    #+
    # methods()
    #-
    def getCameraCommandDialogString(self, name=''):
        s = 'camera command dialog box'
        for e in self._camera.camera_help:
            t = e.split()
            if t[0].lower() == name.lower(): return e
        return s

    #+
    # (command) methods()
    #-
    def initGuiders_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('initGuiders'), ['roiSpec'])
        if self._camera:
            if self.result:
                self._roiSpec = self.result['roiSpec']
                self._camera.logger.debug("calling self._camera.initGuiders('{0:s}')".format(str(self._roiSpec)))
                self._camera.initGuiders(roiSpec=self._roiSpec)
            else:
                self._roiSpec = ''
                self._camera.logger.debug("self._camera.initGuiders('{0:s}') cancelled".format(str(self._roiSpec)))

    def initImage_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('initImage'), ['deltaT'])
        if self._camera:
            if self.result:
                self._deltaT = self.result['deltaT']
                self._camera.logger.debug("calling self._camera.initImage({0:s})".format(str(self._deltaT)))
                self._camera.initImage(deltaT=float(self._deltaT))
            else:
                self._deltaT = ''
                self._camera.logger.debug("self._camera.initImage({0:s}) cancelled".format(str(self._deltaT)))

    def setFilter_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('setFilter'), ['Filter'])
        if self._camera:
            if self.result:
                self._name = self.result['Filter']
                self._camera.logger.debug("calling self._camera.setFilter('{0:s}')".format(str(self._name)))
                self._camera.setFilter(name=self._name)
            else:
                self._name = ''
                self._camera.logger.debug("self._camera.setFilter('{0:s}') cancelled".format(str(self._name)))

    def takeImages_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('takeImages'), ['numImages', 'expTime', 'shutterState', 'scienceActive', 'guidersActive', 'wfsActive', 'imageName'])
        if self._camera:
            if self.result:
                self._numImages = self.result['numImages']
                self._expTime = self.result['expTime']
                self._shutter = ocsGenericEntityLogicDictionary.get(self.result['shutterState'].lower(), False)
                self._science = ocsGenericEntityLogicDictionary.get(self.result['scienceActive'].lower(), False)
                self._guide = ocsGenericEntityLogicDictionary.get(self.result['guidersActive'].lower(), False)
                self._wfs = ocsGenericEntityLogicDictionary.get(self.result['wfsActive'].lower(), False)
                self._imageSequenceName = self.result['imageName']
                self._camera.logger.debug("calling self._camera.takeImages({0:d},{1:.2f},{2:s},{3:s},{4:s},{5:s},'{6:s}')".format(int(self._numImages), 
                    float(self._expTime), str(self._shutter), str(self._science), str(self._guide), str(self._wfs), self._imageSequenceName))
                self._camera.takeImages(numImages=int(self._numImages), expTime=float(self._expTime), shutter=self._shutter, science=self._science, 
                    guide=self._guide, wfs=self._wfs, imageSequenceName=self._imageSequenceName)
            else:
                self._numImages = '0'
                self._expTime = '0.0'
                self._shutter = False
                self._science = False
                self._guide = False
                self._wfs = False
                self._imageSequenceName = ''
                self._camera.logger.debug("self._camera.takeImages({0:d},{1:.2f},{2:s},{3:s},{4:s},{5:s},'{6:s}') cancelled".format(int(self._numImages), 
                    float(self._expTime), str(self._shutter), str(self._science), str(self._guide), str(self._wfs), self._imageSequenceName))

    def clear_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('clear'), ['nClear'])
        if self._camera:
            if self.result:
                self._nclear = self.result['nClear']
                self._camera.logger.debug("calling self._camera.clear('{0:s}')".format(str(self._nclear)))
                self._camera.clear(nClear=int(self._nclear))
            else:
                self._nclear = ''
                self._camera.logger.debug("self._camera.clear('{0:s}') cancelled".format(str(self._nclear)))

    def discardRows_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('discardRows'), ['Rows'])
        if self._camera:
            if self.result:
                self._rows = self.result['Rows']
                self._camera.logger.debug("calling self._cameradiscardRows('{0:s}')".format(str(self._rows)))
                self._cameradiscardRows(rows=int(self._rows))
            else:
                self._rows = ''
                self._camera.logger.debug("self._cameradiscardRows('{0:s}') cancelled".format(str(self._rows)))

    def endImage_handler(self):
        if self._camera:
            if self.result:
                self._camera.endImage()

    def startImage_handler(self):
        OcsEntryDialog(self, self.getCameraCommandDialogString('startImage'), ['shutterState', 'scienceActive', 'guidersActive', 'wfsActive', 'imageName'])
        if self._camera:
            if self.result:
                self._shutter = ocsGenericEntityLogicDictionary.get(self.result['shutterState'].lower(), False)
                self._science = ocsGenericEntityLogicDictionary.get(self.result['scienceActive'].lower(), False)
                self._guide = ocsGenericEntityLogicDictionary.get(self.result['guidersActive'].lower(), False)
                self._wfs = ocsGenericEntityLogicDictionary.get(self.result['wfsActive'].lower(), False)
                self._imageSequenceName = self.result['imageName']
                self._camera.logger.debug("calling self._camera.startImage({0:s},{1:s},{2:s},{3:s},'{4:s}')".format(str(self._shutter), 
                    str(self._science), str(self._guide), str(self._wfs), str(self._imageSequenceName)))
                self._camera.startImage(numImages=int(self._numimages), expTime=float(self._expTime), shutter=self._shutter, science=self._science, 
                    guide=self._guide, wfs=self._wfs, imageSequenceName=self._imageSequenceName)
            else:
                self._shutter = False
                self._science = False
                self._guide = False
                self._wfs = False
                self._imageSequenceName = ''
                self._camera.logger.debug("self._camera.startImage({0:s},{1:s},{2:s},{3:s},'{4:s}') cancelled".format(str(self._shutter), 
                    str(self._science), str(self._guide), str(self._wfs), str(self._imageSequenceName)))

    #+
    # createCameraButtons() method
    #-
    def createCameraButtons(self, _parent=None, system=''):
        self._parent = _parent
        self._system = system
        for e in self._camera.camera_help:
            t = e.split()
            tl = t[0].lower()
            if tl == 'initguiders':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.initGuiders_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=15,sticky=NSEW)
            elif tl == 'initimage':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.initImage_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=16,sticky=NSEW)
            elif tl == 'setfilter':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.setFilter_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=17,sticky=NSEW)
            elif tl == 'takeimages':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.takeImages_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=18,sticky=NSEW)
            elif tl == 'clear':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.clear_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=19,sticky=NSEW)
            elif tl == 'discardrows':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.discardRows_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=20,sticky=NSEW)
            elif tl == 'endimage':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.endImage_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=21,sticky=NSEW)
            elif tl == 'startimage':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.startImage_handler, font=('helvetica', 12, 'normal'), state=DISABLED)
                widget.grid(row=22,sticky=NSEW)
            else:
                pass


#+
# main()
#-
if __name__ == '__main__':
    root = Tk()
    x = OcsCameraEntityGui(root, 'CCS', 'Camera', True)
    if x:
        root.mainloop()
