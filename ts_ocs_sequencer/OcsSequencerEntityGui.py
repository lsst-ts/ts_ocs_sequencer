#!/usr/bin/env python


# +
# imports
# -
from OcsGenericEntityGui import *
from OcsSequencerEntity import *


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityGui.py, contains the code for the (temporary)
TkInter GUI for the OCS Sequencer commandable entity. There are no Python (unit) tests (as yet).

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.


Example:

    root = Tk()
    try:
        x = OcsSequencerEntityGui(parent=root, system='OCS', entity='Sequencer', Standalone=True)
    except OcsSequencerEntityError as e:
        print(e.errstr)
    if x:
        root.mainloop()

API:

    OcsSequencerEntityGui(parent=None, system='OCS', entity='Sequencer', Standalone=True)
        class initializes the OCS sub-system Sequencer entity within the parent frame. If Standalone is True,
        a Quit button is provided. If Standalone is False, no Quit button is created and the object is
        suitable for embedded within other frames (see $TS_OCS_SEQEUNCER_SRC/OcsConsoleGui.py).

CLI:

    The command line interface is provided in a separate class. 
    See $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py for details.

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "OcsSequencerEntityGui.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsSequencerEntityGui() inherits from OcsGenericEntityGui
# -
class OcsSequencerEntityGui(OcsGenericEntityGui):

    # +
    # __init__ method
    # -
    def __init__(self, parent=None, system='OCS', entity='Sequencer', standalone=True):

        # get arguments
        self._parent = parent
        self._system = system
        self._entity = entity
        self._standalone = standalone

        # define some variables and initialize them
        self._command = None
        self._script = None

        # create an instance of this generic entity
        self._sequencer = OcsSequencerEntity(self._system, self._entity, True)

        # now add the GUI stuff
        Frame.__init__(self, self._parent, bd=1, relief=SUNKEN, bg=ocsGenericEntityBackgroundColour.get(
            self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
        self._generic = OcsGenericEntityGui(self._parent, self._system, self._entity, self._standalone)
        Label(self._parent, text=self._system, foreground='blue', bg=ocsGenericEntityBackgroundColour.get(
            self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'normal')).grid(row=0, sticky=NSEW)
        Label(self._parent, text='Sequencer', foreground='blue', bg=ocsGenericEntityBackgroundColour.get(
            self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
            font=('helvetica', 12, 'bold')).grid(row=1, sticky=NSEW)
        self.create_sequencer_buttons(self._parent, self._system)

        self._generic._simFlag.trace('w', self.this_change)

    # +
    # (override trace) method(s)
    # -
    def this_change(self, *args):
        self._sequencer.logger.debug("args = {0:s}".format(str(args)))
        # self._sequencer.logger.debug("self._sequencer._simulate = {0:d}".format(self._sequencer._simulate))
        # self._sequencer.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        simflag = self._generic._simFlag.get()
        self._sequencer._simulate = simflag
        self._generic._this._simulate = simflag
        # self._sequencer.logger.debug("self._generic._this._simulate = {0:d}".format(self._generic._this._simulate))
        # self._sequencer.logger.debug("self._sequencer._simulate = {0:d}".format(self._sequencer._simulate))

    # +
    # methods()
    # -
    def get_sequencer_command_dialog_string(self, name=''):
        s = 'sequencer command dialog box'
        for e1 in self._sequencer.sequencer_help:
            t = e1.split()
            if t[0].lower() == name.lower():
                return e1
        return s

    # +
    # (command) methods()
    # -
    def sequence_handler(self):
        OcsEntryDialog(self, self.get_sequencer_command_dialog_string('sequence_handler'), ['Command'])
        if self._sequencer:
            if self.result:
                self._command = self.result['Command']
                self._sequencer.logger.debug("calling self._sequencer.sequence('{0:s}')".format(
                    str(self._command)))
                self._sequencer.sequence(command=self._command)
            else:
                self._command = ''
                self._sequencer.logger.debug("self._sequencer.sequence('{0:s}') cancelled".format(
                    str(self._command)))

    def script_handler(self):
        OcsEntryDialog(self, self.get_sequencer_command_dialog_string('script_handler'), ['Location'])
        if self._sequencer:
            if self.result:
                self._script = self.result['Location']
                self._sequencer.logger.debug("calling self._sequencer.script_handler('{0:s}')".format(
                    str(self._script)))
                self._sequencer.script(script=self._script)
            else:
                self._script = ''
                self._sequencer.logger.debug("self._sequencer.script_handler('{0:s}') cancelled".format(
                    str(self._script)))

    # +
    # createSequencerButtons() method
    # -
    def create_sequencer_buttons(self, _parent=None, system=''):
        self._parent = _parent
        self._system = system
        for e2 in self._sequencer.sequencer_help:
            t = e2.split()
            tl = t[0].lower()
            if tl == 'sequence':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.sequence_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=15, sticky=NSEW)
            elif tl == 'script':
                widget = Button(self._parent, text=t[0], bg=ocsGenericEntityBackgroundColour.get(
                    self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR),
                    command=self.script_handler, font=('helvetica', 12, 'normal'), state=NORMAL)
                widget.grid(row=16, sticky=NSEW)
            else:
                pass


# +
# main()
# -
if __name__ == '__main__':
    root = Tk()
    x = OcsSequencerEntityGui(root, 'OCS', 'Sequencer', True)
    if x:
        root.mainloop()
