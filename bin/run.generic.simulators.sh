#!/bin/sh

xterm -bg black -fg yellow -geometry 200x30+0+0   -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS Archiver Simulator"          -e python $TS_OCS_SEQUENCER_SRC/OcsGenericSimulator.py Archiver          &
xterm -bg black -fg yellow -geometry 200x30+10+10 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS Camera Simulator"            -e python $TS_OCS_SEQUENCER_SRC/OcsGenericSimulator.py Camera            &
xterm -bg black -fg yellow -geometry 200x30+20+20 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS CatchupArchiver Simulator"   -e python $TS_OCS_SEQUENCER_SRC/OcsGenericSimulator.py CatchupArchiver   &
xterm -bg black -fg yellow -geometry 200x30+30+30 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS ProcessingCluster Simulator" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericSimulator.py ProcessingCluster &
xterm -bg black -fg yellow -geometry 200x30+40+40 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS Tcs Simulator"               -e python $TS_OCS_SEQUENCER_SRC/OcsGenericSimulator.py Tcs               &
