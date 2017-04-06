#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsCameraEntity import *


# +
# main()
# -
if __name__ == '__main__':

    telescope = None
    try:
        telescope = OcsGenericEntity('TCS', 'Tcs', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if telescope:

        # disable
        telescope.logger.info('telescope.disable()')
        telescope.disable()

        # standby
        telescope.logger.info('telescope.standby()')
        telescope.standby()

        # exit control
        telescope.logger.info('telescope.exitcontrol()')
        telescope.exitcontrol()

        # execute destructor
        telescope.logger.info('del telescope')
        del telescope
