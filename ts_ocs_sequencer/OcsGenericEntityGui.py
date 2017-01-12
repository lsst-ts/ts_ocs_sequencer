#!/usr/bin/env python

#+
# imports
#-
from OcsGenericEntity import *
from OcsGui import *
import sys

#+
# globals
#-
BG_DEFAULT = '#f0f8ff'
bgColours = {
    'ATCS'  : '#fff8dc',
    'CALCS' : '#fffff0',
    'CCS'   : '#fffacd',
    'DMCS'  : '#fff5ee',
    'EMCS'  : '#f0fff0',
    'SFCS'  : '#f5fffa',
    'TCS'   : '#f0ffff',
    'TEST'  : BG_DEFAULT
}

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
        self._this = OcsGenericEntity( self._system, self._entity, False)
        if self._this:
            self._this.logger.info("Created ENTITY OK")

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=bgColours.get(self._system,BG_DEFAULT))
        Label(self._parent, text=self._system, foreground='blue', bg=bgColours.get(self._system,BG_DEFAULT), font=('helvetica', 12, 'normal')).grid(row=0,sticky=NSEW)
        Label(self._parent, text=self._entity, foreground='blue', bg=bgColours.get(self._system,BG_DEFAULT), font=('helvetica', 12, 'bold')).grid(row=1,sticky=NSEW)
        self.createGenericButtons(self._parent,self._system)

        self._simFlag = BooleanVar()
        self._simFlag.set(False)
        self._simulation = self._simFlag.get()
        self._this._simulation = self._simFlag.get()

        widget = Checkbutton(self._parent, text='Simulation', variable=self._simFlag)
        widget.config(foreground='black', bg=bgColours.get(self._system,BG_DEFAULT), font=('helvetica', 10, 'roman'))
        widget.grid(row=2,sticky=NSEW)

        self._simFlag.trace('w',self.simChange)
        self._simFlag.set(True)

        if self._standalone:
            OcsQuitButton(self._parent).grid(row=12,sticky=NSEW)

    #+
    # callback method(s)
    #-
    def simChange(self,*args):
        val = self._simFlag.get()
        self._simulation = val
        self._this._simulation = val

    #+
    # deferred methods()
    #-
    def getCommandDialogString(self,name=''):
        s = 'generic command dialog box'
        for e in self._this.generic_help:
            t = e.split()
            if t[0].lower() == name.lower(): return e
        return s

    def handleSetValue(self):
        OcsEntryDialog(self,self.getCommandDialogString('setvalue'),['Parameter','Value'])
        if self.result:
            self._this._parameter = self.result['Parameter']
            self._this._value     = self.result['Value']
            self._this.setvalue(parameter=self._this._parameter, value=self._this._value)

    def handleStart(self):
        x = OcsEntryDialog(self, self.getCommandDialogString('start'), ['StartId'])
        if self.result:
            self._this._startid = self.result['StartId']
            self._this.logger.info("Calling start(startid)")
            self._this.start(startid=self._this._startid)

    def handleStop(self):
        OcsEntryDialog(self,self.getCommandDialogString('stop'),['Device'])
        if self.result:
            self._this._device = self.result['Device']
            self._this.stop(device=self._this._device)

    #+
    # createGenericButtons() method
    #-
    def createGenericButtons(self,_parent=None,system=''):
        self._parent = _parent
        self._system = system
        #for e in self._this().generic_help:
        for e in OcsGenericEntity(self._system, self._entity).generic_help:
            t = e.split()
            tl = t[0].lower()
            if tl == 'abort':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.abort)
                widget.grid(row=3,sticky=NSEW)
            elif tl == 'disable':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.disable)
                widget.grid(row=4,sticky=NSEW)
            elif tl == 'enable':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.enable)
                widget.grid(row=5,sticky=NSEW)
            elif tl == 'entercontrol':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.entercontrol)
                widget.grid(row=6,sticky=NSEW)
            elif tl == 'exitcontrol':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.exitcontrol)
                widget.grid(row=7,sticky=NSEW)
            elif tl == 'setvalue':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self.handleSetValue)
                widget.grid(row=8,sticky=NSEW)
            elif tl == 'start':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self.handleStart)
                widget.grid(row=9,sticky=NSEW)
            elif tl == 'standby':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self._this.standby)
                widget.grid(row=10,sticky=NSEW)
            elif tl == 'stop':
                widget = Button(self._parent, text=t[0], bg=bgColours.get(self._system,BG_DEFAULT), command=self.handleStop)
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
