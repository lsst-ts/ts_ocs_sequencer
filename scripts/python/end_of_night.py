#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *

import threading
import os

# +
# function: EndOfNight()
# -
def EndOfNight(entity='', entobj=None):

    # check input(s)
    if (not isinstance(entity, str) or entity == '') or (not entobj):
        return

    # do start_of_night stuff
    if entobj:

        # disable
        entobj.logger.info('{0:s}.disable()'.format(entity))
        entobj.disable()

        # standby
        entobj.logger.info("{0:s}.standby()".format(entity))
        entobj.standby()

        # exit control
        entobj.logger.info('{0:s}.enable()'.format(entity))
        entobj.exitcontrol()

    # return
    return

# +
# main()
# -
if __name__ == "__main__":

    # create generic commandable entities
    archiver = OcsGenericEntity('DMCS', 'Archiver', False)
    camera = OcsGenericEntity('CCS', 'Camera', False)
    catchuparchiver = OcsGenericEntity('DMCS', 'CatchupArchiver', False)
    processingcluster = OcsGenericEntity('DMCS', 'ProcessingCluster', False)
    tcs = OcsGenericEntity('TCS', 'Tcs', False)

    # create jobs for each entity:
    jobs = []
    for E in ( archiver, catchuparchiver, camera, processingcluster, tcs ):
        j = threading.Thread(target=EndOfNight, args=(E._entity, E))
        jobs.append(j)
        j.start()

    for j in jobs:
        j.join()
        print('{0:s} exited'.format(j.name))
