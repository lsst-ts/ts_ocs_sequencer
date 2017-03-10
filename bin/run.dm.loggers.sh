#!/bin/sh

xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS Archiver Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_archiverEntitySummaryState.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS CatchupArchiver Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_catchuparchiverEntitySummaryState.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS ProcessingCluster Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_processingclusterEntitySummaryState.py &
