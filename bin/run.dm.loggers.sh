#!/bin/sh

xterm -bg black -fg green -geometry 200x30+0+0 -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS Archiver Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_archiverEntitySummaryState.py &
xterm -bg black -fg green -geometry 200x30+10+10 -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS CatchupArchiver Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_catchuparchiverEntitySummaryState.py &
xterm -bg black -fg green -geometry 200x30+20+20 -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS ProcessingCluster Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_processingclusterEntitySummaryState.py &
