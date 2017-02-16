#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsSequencerEntity import *


# +
# main()
# -
if __name__ == '__main__':

    sequencer = None
    try:
        sequencer = OcsSequencerEntity('OCS', 'ocs', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if sequencer:

        # disable
        sequencer.logger.info('sequencer.disable()')
        sequencer.disable()

        # standby
        sequencer.logger.info('sequencer.standby()')
        sequencer.standby()

        # exit control
        sequencer.logger.info('sequencer.exitcontrol()')
        sequencer.exitcontrol()

        # execute destructor
        sequencer.logger.info('del sequencer')
        del sequencer
