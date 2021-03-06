#!/bin/sh

xterm -fg -black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS Archiver Simulator" -e python $TS_OCS_SEQUENCER_SRC/OcsArchiverThreads.py &
xterm -fg black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS CatchupArchiver Simulator" -e python $TS_OCS_SEQUENCER_SRC/OcsCatchupArchiverThreads.py &
xterm -fg black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS ProcessingCluster Simulator" -e python $TS_OCS_SEQUENCER_SRC/OcsProcessingClusterThreads.py &
