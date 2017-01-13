#!/usr/bin/env python


#+
# imports
#-
from OcsGenericEntity import *
from OcsGui import *
import sys


#+
# class: OcsGenericEntityGui() inherits from Frame
#-
class OcsGenericEntityGui(Frame):

    #+
    # __init__ method
    #-
    def __init__(self, parent=None, system='', entity='', standalone=True):

        # get arguments
        self._parent = parent
        self._system = system
        self._entity = entity
        self._standalone = standalone

        # create an instance of this generic entity
        self._this = OcsGenericEntity(self._system, self._entity, False)

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
        Label(self._parent, text=self._system, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'normal')).grid(row=0,sticky=NSEW)
        Label(self._parent, text=self._entity, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'bold')).grid(row=1,sticky=NSEW)
        self.createGenericButtons(self._parent,self._system)

        self._simFlag = BooleanVar()
        self._simFlag.set(False)
        self._this._simulate = self._simFlag.get()
        self._this.logger.debug("self._this._simulate = {0:d}".format(self._this._simulate))

        widget = Checkbutton(self._parent, text='Simulation', variable=self._simFlag)
        widget.config(foreground='black', bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), font=('helvetica', 10, 'roman'))
        widget.grid(row=2,sticky=NSEW)

        self._simFlag.trace('w',self.simChange)
        self._simFlag.set(True)

        if self._standalone:
            OcsQuitButton(self._parent).grid(row=12,sticky=NSEW)

    #+
    # (trace) method(s)
    #-
    def simChange(self, *args):
        self._this.logger.debug("self._this._simulate = {0:d}".format(self._this._simulate))
        self._this._simulate = self._simFlag.get()
        self._this.logger.debug("self._this._simulate = {0:d}".format(self._this._simulate))

    #+
    # (deferred) methods()
    #-
    def getCommandDialogString(self, name=''):
        s = 'generic command dialog box'
        for e in self._this.generic_help:
            t = e.split()
            if t[0].lower() == name.lower(): return e
        return s

    #+
    # (command) methods()
    #-
    def abort_handler(self):
        if self._this:
            self._this.abort()

    def disable_handler(self):
        if self._this:
            self._this.disable()

    def enable_handler(self):
        if self._this:
            self._this.enable()

    def entercontrol_handler(self):
        if self._this:
            self._this.entercontrol()

    def exitcontrol_handler(self):
        if self._this:
            self._this.exitcontrol()

    def setvalue_handler(self):
        OcsEntryDialog(self, self.getCommandDialogString('setvalue'), ['Parameter','Value'])
        if self._this and self.result:
            self._parameter = self.result['Parameter']
            self._value = self.result['Value']
            self._this.setvalue(parameter=self._parameter, value=self._value)

    def standby_handler(self):
        if self._this:
            self._this.standby()

    def start_handler(self):
        OcsEntryDialog(self, self.getCommandDialogString('start'),  ['StartId'])
        if self._this and self.result:
            self._startid = self.result['StartId']
            self._this.start(startid=self._startid)

    def stop_handler(self):
        OcsEntryDialog(self, self.getCommandDialogString('stop'), ['Device'])
        if self._this and self.result:
            self._device = self.result['Device']
            self._this.stop(device=self._device)

    #+
    # createGenericButtons() method
    #-
    def createGenericButtons(self, _parent=None, system=''):
        self._parent = _parent
        self._system = system
        for e in self._this.generic_help:
            t = e.split()
            tl = t[0].lower()
            if tl == 'abort':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.abort_handler)
                widget.grid(row=3,sticky=NSEW)
            elif tl == 'disable':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.disable_handler)
                widget.grid(row=4,sticky=NSEW)
            elif tl == 'enable':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.enable_handler)
                widget.grid(row=5,sticky=NSEW)
            elif tl == 'entercontrol':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.entercontrol_handler)
                widget.grid(row=6,sticky=NSEW)
            elif tl == 'exitcontrol':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.exitcontrol_handler)
                widget.grid(row=7,sticky=NSEW)
            elif tl == 'setvalue':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.setvalue_handler)
                widget.grid(row=8,sticky=NSEW)
            elif tl == 'start':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.start_handler)
                widget.grid(row=9,sticky=NSEW)
            elif tl == 'standby':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.standby_handler)
                widget.grid(row=10,sticky=NSEW)
            elif tl == 'stop':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR), command=self.stop_handler)
                widget.grid(row=11,sticky=NSEW)
            else:
                pass

#+
# main()
#-
if __name__ == '__main__':
    root = Tk()
    x = OcsGenericEntityGui(root, 'CCS', 'Camera', True)
    if x:
        root.mainloop()
