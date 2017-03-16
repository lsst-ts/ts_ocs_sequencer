#!/bin/sh

xterm -fg black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS Archiver" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py Archiver &
xterm -fg black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS CatchupArchiver" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py CatchupArchiver &
xterm -fg black -bg "#fff5ee" -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS ProcessingCluster" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py ProcessingCluster &
