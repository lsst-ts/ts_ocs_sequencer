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

        # set filter
        camera.logger.info('camera.filter(\'g-9\', 60)')
        camera.setFilter('g-9', 60)

        # init image
        camera.logger.info('camera.initImage(4.0, 10)')
        camera.initImage(4.0, 10)

        # take image
        isn = ocs_id(True)
        camera.logger.info('camera takeImages(2, 15.0, True, True, False, False, {0:s}, 45)',format(isn))
        camera.takeImages(2, 15.0, True, True, False, False, isn, 45)

        # execute destructor
        camera.logger.info('del camera')
        del camera
