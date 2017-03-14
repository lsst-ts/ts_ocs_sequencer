#!/usr/bin/env python


# +
# imports
# -
from OcsCameraEntityGui import *
from OcsSequencerEntityGui import *
import functools


# +
# __doc__ string
# -
__doc__ = """


This file, $TS_OCS_SEQUENCER_SRC/OcsConsoleGui.py, contains the code for the (temporary)
TkInter GUI consolei for all commandable entities. There are no Python (unit) tests (as yet).

Behavioural commands are handled on a per commandable entity basis using a derived class.

Note that certain commands are only available within certain states as described in LSE-209.

Example:

    root = Tk()
    try:
        x = OcsConsoleGui(parent=root)
    except:
        pass
    if x:
        root.mainloop()

API:

    OcsConsoleGui(parent=None)
        class initializes the console within the parent frame. It provides a control panel
        of checkbuttons for each commandable entity which is instantiated on checking the
        appropriate box. Re-checking the box will hide the given commandable entity.

CLI:

    The command line interface is provided in a separate class. 
    See $TS_OCS_SEQUENCER_SRC/OcsConsoleGui.py for details.

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
# class: OcsConsoleGui() inherits from Frame
# -
class OcsConsoleGui(Frame):

    # +
    # __init__ method
    # -
    def __init__(self, parent=None):

        # get arguments
        self._parent = parent

        # initialize the master frame
        Frame.__init__(self, self._parent)
        self._master = OcsFrameGroup(self._parent)
        self._master.pack(in_=self._parent, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)

        # create console frame
        self._console = self._master.add_console(self._master, 'OCS', 'Console')

        # create entity frames
        for self._system in sorted(ocsGenericEntityEntityDictionary):
            for self._entity in ocsGenericEntityEntityDictionary[self._system]:
                self._widget = self._master.add_frame(self._master, self._system, self._entity)

        # populate the console panel
        self._master.populate_console(self._console)


# +
# class: OcsFrameGroup() inherits from the Frame class
# -
class OcsFrameGroup(Frame):

    # +
    # method: __init__
    # -
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self._parent = parent
        self._frames = {}
        self._guis = {}
        self._systems = {}
        self._vars = {}
        self._widgets = {}

        self._parent = None
        self._system = None
        self._entity = None

    # +
    # method: add_console()
    # -
    def add_console(self, parent=None, system='', entity=''):
        self._parent = parent
        self._system = system
        self._entity = entity
        if self._parent and (isinstance(self._system, str) and self._system != '') and \
                (isinstance(self._entity, str) and self._entity != ''):
            self._frames[self._entity] = Frame(self._parent, relief=SUNKEN, bd=5,
                                               bg=ocsGenericEntityBackgroundColour.get(
                                                   self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
            self._frames[self._entity].pack(in_=self._parent, side=LEFT, ipadx=0, ipady=0,
                                            padx=0, pady=0, fill=BOTH, expand=False)
            self._systems[self._entity] = self._system
        else:
            self._frames[self._entity] = None
        return self._frames[self._entity]

    # +
    # method: add_frame()
    # -
    def add_frame(self, parent=None, system='', entity=''):
        self._parent = parent
        self._system = system
        self._entity = entity
        if self._parent and (isinstance(self._system, str) and self._system != '') \
                and (isinstance(self._entity, str) and self._entity != ''):
            self._frames[self._entity] = Frame(self._parent, relief=SUNKEN, bd=2,
                                               bg=ocsGenericEntityBackgroundColour.get(
                                                   self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
            self._frames[self._entity].pack(in_=self._parent, side=LEFT, ipadx=0, ipady=0,
                                            padx=0, pady=0, fill=BOTH, expand=False)
            self._systems[self._entity] = self._system
        else:
            self._frames[self._entity] = None
        return self._frames[self._entity]

    # +
    # method: populate_console()
    # -
    def populate_console(self, parent=None):
        self._parent = parent
        if self._parent:
            for self._system in sorted(ocsGenericEntityEntityDictionary):
                for self._entity in ocsGenericEntityEntityDictionary[self._system]:
                    self._guis[self._entity] = None
                    self._vars[self._entity] = BooleanVar()
                    self._vars[self._entity].trace("w", self.get_change)
                    self._widgets[self._entity] = Checkbutton(self._parent, text='{0:s} {1:s}'.format(
                        self._system, self._entity),
                        variable=self._vars[self._entity], anchor=W, onvalue=True, offvalue=False)
                    self._widgets[self._entity].config(foreground='black', font=('helvetica', 10, 'roman'),
                                                       background=ocsGenericEntityBackgroundColour.get(
                                                           self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
                    self._widgets[self._entity].pack(in_=self._parent, side=TOP, ipadx=0, ipady=0,
                                                     padx=0, pady=0, fill=BOTH, expand=YES)
                    self._vars[self._entity].set(False)

    # +
    # method: get_change()
    # -
    def get_change(self, *args):
        print('get_change> args = {0:s}'.format(str(args)))
        for El in self._vars:
            # show
            if self._vars[El].get():
                # print('get_change> self._vars[{0:s}].get() = {1:s}'.format(E, str(self._vars[E].get())))
                if self._guis[El]:
                    self._frames[El].pack(side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
                    self._guis[El].pack(in_=self._frames[El], side=LEFT, ipadx=0, ipady=0,
                                        padx=0, pady=0, fill=BOTH, expand=YES)
                else:
                    # print('get_change> self._vars[{0:s}] = {1:s}'.format(E, str(self._vars[E])))
                    try:
                        if El.lower() == 'ocs':
                            cls = self._s2c('Ocs{0:s}EntityGui'.format('Sequencer'))
                        elif El.lower() == 'camera':
                            cls = self._s2c('Ocs{0:s}EntityGui'.format('Camera'))
                        else:
                            cls = self._s2c('Ocs{0:s}EntityGui'.format(El))
                    except AttributeError:
                        cls = None
                    # print('get_change> cls = {0:s}'.format(str(cls)))
                    if cls:
                        self._frames[El].pack(side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
                        self._guis[El] = cls(self._frames[El], self._systems[El], El, False)
            # hide
            else:
                # print('get_change> self._vars[{0:s}].get() = {1:s}'.format(E, str(self._vars[E].get())))
                self._frames[El].pack_forget()
                if self._guis[El]:
                    self._guis[El].pack_forget()

    # +
    # (hidden) method: _s2c()
    # -
    @staticmethod
    def _s2c(instr=''):
        return functools.reduce(getattr, instr.split('.'), sys.modules[__name__])


# +
# main()
# -
if __name__ == '__main__':
    root = Tk()
    x = OcsConsoleGui(root)
    if x:
        root.mainloop()
