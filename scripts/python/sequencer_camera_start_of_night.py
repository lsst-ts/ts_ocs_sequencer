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
        cmd = 'enterControl entity=camera'
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # start
        startid = [sys.argv[1] if len(sys.argv)>1 else 'Normal']
        cmd = 'start entity=camera startid={0:s}'.format(startid[0])
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # enable
        cmd = 'enable entity=camera'
        msg = "sequencer.sequence('{0:s}')".format(cmd)
        sequencer.logger.info(msg)
        sequencer.sequence(cmd)

        # execute destructor
        sequencer.logger.info('del sequencer')
        del sequencer
