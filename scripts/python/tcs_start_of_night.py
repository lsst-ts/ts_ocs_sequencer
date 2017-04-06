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

        # enter control
        telescope.logger.info('telescope.entercontrol()')
        telescope.entercontrol()

        # start
        startid = [sys.argv[1] if len(sys.argv)>1 else 'Normal']
        telescope.logger.info("telescope.start('{0:s}')".format(startid[0]))
        telescope.start(startid[0])

        # enable
        telescope.logger.info('telescope.enable()')
        telescope.enable()

        # execute destructor
        telescope.logger.info('del telescope')
        del telescope
