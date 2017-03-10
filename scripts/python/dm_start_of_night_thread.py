#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *

import threading
import os

# +
# function: worker()
# -
def worker(entity='', entobj=None):

    # debug output
    print('name: {0:s}'.format(threading.currentThread().getName()))
    print('entity: {0:s}'.format(entity))
    if hasattr(os, 'getppid'):
        print('parent process id: {0:s}'.format(str(os.getppid())))
    if hasattr(os, 'getpid'):
        print('process id: {0:s}'.format(str(os.getpid())))

    # do start_of_night stuff
    if entobj:

        # enter control
        entobj.logger.info('{0:s}.entercontrol()'.format(entity))
        entobj.entercontrol()

        # start
        cfg = '{0:s}-Normal'.format(entity.lower())
        entobj.logger.info("{0:s}.start('{1:s}')".format(entity, cfg))
        entobj.start(cfg)

        # enable
        entobj.logger.info('{0:s}.enable()'.format(entity))
        entobj.enable()

    # return
    return

# +
# main()
# -
if __name__ == "__main__":

    # created shared entities
    archiver = OcsGenericEntity('DMCS', 'Archiver', False)
    catchuparchiver = OcsGenericEntity('DMCS', 'CatchupArchiver', False)
    processingcluster = OcsGenericEntity('DMCS', 'ProcessingCluster', False)

    # create jobs for each entity:
    jobs = []
    for E in ( archiver, catchuparchiver, processingcluster ):
        j = threading.Thread(target=worker, args=(E._entity, E))
        jobs.append(j)
        j.start()

    for j in jobs:
        j.join()
        print('{0:s} exited'.format(j.name))
