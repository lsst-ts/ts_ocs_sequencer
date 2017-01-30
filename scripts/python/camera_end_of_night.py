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

    camera = None
    try:
        camera = OcsCameraEntity('CCS', 'Camera', False)
    except OcsCameraEntityException as e:
        print(e.errstr)

    if camera:

        # disable
        camera.logger.info('camera.disable()')
        camera.disable()

        # standby
        camera.logger.info('camera.standby()')
        camera.standby()

        # exit control
        camera.logger.info('camera.exitcontrol()')
        camera.exitcontrol()

        # execute destructor
        camera.logger.info('del camera')
        del camera
