#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsCameraEntity import *
from OcsSequencerEntity import *

import multiprocessing
import os

# +
# function: worker_code()
# -
def worker_code(entity='', entobj=None):

    # debug output
    print('name: {0:s}'.format(multiprocessing.current_process().name))
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
        entobj.logger.info("{0:s}.start('Normal')".format(entity))
        entobj.start('Normal')

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
    camera    = OcsCameraEntity('CCS', 'Camera', False)
    sequencer = OcsSequencerEntity('OCS', 'ocs', False)

    # create jobs for each entity:
    jobs = []
    for E in ( camera, sequencer ):
        j = multiprocessing.Process(target=worker_code, args=(E._entity, E))
        jobs.append(j)
        j.start()

    for j in jobs:
        j.join()
        print('{0:s}.exitcode: {1:s}'.format(j.name, str(j.exitcode)))
