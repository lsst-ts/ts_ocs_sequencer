#!/usr/bin/env python


#+
# imports
#-
from OcsCameraEntityGui import *
from OcsSequencerEntityGui import *


#+
# class: OcsConsoleGui() inherits from Frame
#-
class OcsConsoleGui(Frame):

    #+
    # __init__ method
    #-
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

    #+
    # method: __init__
    #-
    def __init__(self, parent=None):
        self._parent = parent
        Frame.__init__(self, self._parent)
        self._frames = {}
        self._guis = {}
        self._systems = {}
        self._vars = {}
        self._widgets = {}

    #+
    # method: add_console()
    #-
    def add_console(self, parent=None, system='', entity=''):
        self._parent = parent
        self._system = system
        self._entity = entity
        if self._parent and (isinstance(self._system,str) and self._system!='') and (isinstance(self._entity,str) and self._entity!=''):
            self._frames[self._entity] = Frame(self._parent, relief=SUNKEN, bd=5, bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
            self._frames[self._entity].pack(in_=self._parent, side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=False)
            self._systems[self._entity] = self._system
        else:
            self._frames[self._entity] = None
        return self._frames[self._entity]

    #+
    # method: add_frame()
    #-
    def add_frame(self, parent=None, system='', entity=''):
        self._parent = parent
        self._system = system
        self._entity = entity
        if self._parent and (isinstance(self._system,str) and self._system!='') and (isinstance(self._entity,str) and self._entity!=''):
            self._frames[self._entity] = Frame(self._parent, relief=SUNKEN, bd=2, bg=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
            self._systems[self._entity] = self._system
        else:
            self._frames[self._entity] = None
        return self._frames[self._entity]

    #+
    # method: populate_console()
    #-
    def populate_console(self, parent=None):
        self._parent = parent
        if self._parent:
            for self._system in sorted(ocsGenericEntityEntityDictionary):
                for self._entity in ocsGenericEntityEntityDictionary[self._system]:
                    self._vars[self._entity] = BooleanVar()
                    self._vars[self._entity].set(True)
                    self._widgets[self._entity] = Checkbutton(self._parent, text='{0:s} {1:s}'.format(self._system, self._entity), 
                        variable=self._vars[self._entity], anchor=W, onvalue=True, offvalue=False)
                    self._widgets[self._entity].config(foreground='black', font=('helvetica', 10, 'roman'),
                        background=ocsGenericEntityBackgroundColour.get(self._system, OCS_GENERIC_ENTITY_BACKGROUND_COLOUR))
                    self._widgets[self._entity].pack(in_=self._parent, side=TOP, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
                    self._vars[self._entity].trace("w", self.get_change)
                    self._guis[self._entity] = None
                    self._vars[self._entity].set(False)
                    self._vars[self._entity].set(False)

    #+
    # method: get_change()
    #-
    def get_change(self, *args):
        for E in self._vars:
            # show
            if self._vars[E].get():
                self._frames[E].pack(side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
                if self._guis[E] == None:
                    try:
                        cls = self._s2c('Ocs{0:s}EntityGui'.format(E))
                    except AttributeError:
                        cls = None
                    if cls != None:
                        self._guis[E] = cls(self._frames[E], self._systems[E], E, False)
                        self._guis[E].pack(in_=self._frames[E], side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
                else:
                    self._guis[E].pack(in_=self._frames[E], side=LEFT, ipadx=0, ipady=0, padx=0, pady=0, fill=BOTH, expand=YES)
            # hide
            else:
                if self._guis[E] != None:
                    self._guis[E].pack_forget()
                    self._frames[E].pack_forget()

    #+
    # (hidden) method: _s2c()
    #-
    def _s2c(self, instr=''):
       return reduce(getattr, instr.split('.'), sys.modules[__name__])


# main()
# -
if __name__ == '__main__':
    root = Tk()
    x = OcsConsoleGui(root)
    if x:
        root.mainloop()
