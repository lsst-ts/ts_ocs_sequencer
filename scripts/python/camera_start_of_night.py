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

        # enter control
        camera.logger.info('camera.entercontrol()')
        camera.entercontrol()

        # start
        startid = [sys.argv[1] if len(sys.argv)>1 else 'Normal']
        camera.logger.info("camera.start('{0:s}')".format(startid[0]))
        camera.start(startid[0])

        # enable
        camera.logger.info('camera.enable()')
        camera.enable()

        # execute destructor
        camera.logger.info('del camera')
        del camera
