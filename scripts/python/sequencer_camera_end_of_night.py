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

        # disable control
        cmd = 'disable entity=camera'
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # standby
        cmd = 'standby entity=camera'
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # exitControl
        cmd = 'exitControl entity=camera'
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # execute destructor
        sequencer.logger.info('del sequencer')
        del sequencer
