#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsGenericEntity import *
import threading
import os


# +
# function: ocs_end_of_night()
# -
def ocs_end_of_night(entity_name='', entity_object=None):

    # check input(s)
    if (not isinstance(entity_name, str) or entity_name == '') or (not entity_object):
        return

    # do end of night stuff
    if entity_object:

        # disable
        entity_object.logger.info('{0:s}.disable()'.format(entity_name))
        entity_object.disable()

        # standby
        entity_object.logger.info("{0:s}.standby()".format(entity_name))
        entity_object.standby()

        # exit control
        entity_object.logger.info('{0:s}.exitcontrol()'.format(entity_name))
        entity_object.exitcontrol()

    # return
    return

# +
# function: ocs_end_of_night_main()
# -
def ocs_end_of_night_main(*args):

    # create jobs for each argument:
    jobs = []
    for E in args:
        j = threading.Thread(target=ocs_end_of_night, args=(E._entity, E))
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
    ocs_end_of_night_main(OcsGenericEntity('DMCS', 'Archiver', False), 
         OcsGenericEntity('CCS', 'Camera', False), 
         OcsGenericEntity('DMCS', 'CatchupArchiver', False), 
         OcsGenericEntity('DMCS', 'ProcessingCluster', False), 
         OcsGenericEntity('TCS', 'Tcs', False))
