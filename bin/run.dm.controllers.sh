#!/bin/sh

xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS Archiver" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py Archiver &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS CatchupArchiver" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py CatchupArchiver &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T "DMCS ProcessingCluster" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py ProcessingCluster &
