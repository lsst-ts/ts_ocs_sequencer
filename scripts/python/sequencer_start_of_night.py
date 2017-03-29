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
        sequencer = OcsSequencerEntity('OCS', 'Sequencer', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if sequencer:

        # enter control
        sequencer.logger.info('sequencer.entercontrol()')
        sequencer.entercontrol()

        # start
        startid = [sys.argv[1] if len(sys.argv)>1 else 'Sequencer-Normal']
        sequencer.logger.info("sequencer.start('{0:s}')".format(startid[0]))
        sequencer.start(startid[0])

        # enable
        sequencer.logger.info('sequencer.enable()')
        sequencer.enable()

        # execute destructor
        sequencer.logger.info('del sequencer')
        del sequencer
