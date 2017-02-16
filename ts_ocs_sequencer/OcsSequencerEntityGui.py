#!/usr/bin/env python


#+
# imports
#-
from OcsGenericEntityGui import *
from OcsSequencerEntity import *


#+
# class: OcsSequencerEntityGui() inherits from OcsGenericEntityGui
#-
class OcsSequencerEntityGui(OcsGenericEntityGui):

    #+
    # __init__ method
    #-
    def __init__(self, parent=None, system='OCS', entity='ocs', standalone=True):

        # get arguments
        self._parent = parent
        self._system = system
        self._entity = entity
        self._standalone = standalone

        # create an instance of this generic entity
        self._sequencer = OcsSequencerEntity(self._system, self._entity, True)

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
        self._generic = OcsGenericEntityGui(self._parent, self._system, self._entity, self._standalone)
        Label(self._parent, text=self._system, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'normal')).grid(row=0,sticky=NSEW)
        Label(self._parent, text='Sequencer', foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'bold')).grid(row=1,sticky=NSEW)
        #Label(self._parent, text=self._entity, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
        #    font=('helvetica', 12, 'bold')).grid(row=1,sticky=NSEW)
        self.createSequencerButtons(self._parent,self._system)

        self._generic._simFlag.trace('w',self.thisChange)

    #+
    # (override trace) method(s)
    #-
    def thisChange(self, *args):
        self._sequencer.logger.debug("self._sequencer._simulate = {0:d}".format(self._sequencer._simulate))
        self._sequencer.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        self._sequencer._simulate = self._generic._this._simulate = self._generic._simFlag.get()
        self._sequencer.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        self._sequencer.logger.debug("self._sequencer._simulate = {0:d}".format(self._sequencer._simulate))

    #+
    # methods()
    #-
    def getSequencerCommandDialogString(self, name=''):
        s = 'sequencer command dialog box'
        for e in self._sequencer.sequencer_help:
            t = e.split()
            if t[0].lower() == name.lower(): return e
        return s

    #+
    # (command) methods()
    #-
    def sequence_handler(self):
        OcsEntryDialog(self, self.getSequencerCommandDialogString('sequence_handler'), ['Command'])
        if self._sequencer:
            if self.result:
                self._command = self.result['Command']
                self._sequencer.logger.debug("calling self._sequencer.sequence('{0:s}')".format(str(self._command)))
                self._sequencer.sequence(command=self._command)
            else:
                self._command = ''
                self._sequencer.logger.debug("self._sequencer.sequence('{0:s}') cancelled".format(str(self._command)))

    def script_handler(self):
        OcsEntryDialog(self, self.getSequencerCommandDialogString('script_handler'), ['Location'])
        if self._sequencer:
            if self.result:
                self._script = self.result['Location']
                self._sequencer.logger.debug("calling self._sequencer.script_handler('{0:s}')".format(str(self._script)))
                self._sequencer.script_handler(script=self._script)
            else:
                self._script = ''
                self._sequencer.logger.debug("self._sequencer.script_handler('{0:s}') cancelled".format(str(self._script)))

    #+
    # createSequencerButtons() method
    #-
    def createSequencerButtons(self, _parent=None, system=''):
        self._parent = _parent
        self._system = system
        for e in self._sequencer.sequencer_help:
            t = e.split()
            tl = t[0].lower()
            if tl == 'sequence':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.sequence_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=15,sticky=NSEW)
            elif tl == 'script':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(self._system,OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.script_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=16,sticky=NSEW)
            else:
                pass


#+
# main()
#-
if __name__ == '__main__':
    root = Tk()
    x = OcsSequencerEntityGui(root, 'OCS', 'ocs', True)
    if x:
        root.mainloop()
