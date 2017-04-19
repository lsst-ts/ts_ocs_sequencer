#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *
import threading
import os


# +
# function: ocs_start_of_night()
# -
def ocs_start_of_night(entity_name='', entity_object=None):

    # check input(s)
    if (not isinstance(entity_name, str) or entity_name == '') or (not entity_object):
        return

    # do start of night stuff
    if entity_object:

        # enter control
        entity_object.logger.info('{0:s}.entercontrol()'.format(entity_name))
        entity_object.entercontrol()

        # start
        cfg = 'Normal'
        entity_object.logger.info("{0:s}.start('{1:s}')".format(entity_name, cfg))
        entity_object.start(cfg)

        # enable
        entity_object.logger.info('{0:s}.enable()'.format(entity_name))
        entity_object.enable()

    # return
    return

# +
# function: ocs_start_of_night_main()
# -
def ocs_start_of_night_main(*args):

    # create jobs for each argument:
    jobs = []
    for E in args:
        j = threading.Thread(target=ocs_start_of_night, args=(E._entity, E))
        jobs.append(j)
        j.start()

    # wait for completion of all jobs
    for j in jobs:
        j.join()
        print('{0:s} exited'.format(j.name))


# +
# main entry point
# -
if __name__ == "__main__":
    ocs_start_of_night_main(OcsGenericEntity('DMCS', 'Archiver', False), 
         OcsGenericEntity('CCS', 'Camera', False), 
         OcsGenericEntity('DMCS', 'CatchupArchiver', False), 
         OcsGenericEntity('DMCS', 'ProcessingCluster', False), 
         OcsGenericEntity('TCS', 'Tcs', False))
