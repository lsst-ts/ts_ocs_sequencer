#!/bin/sh

xterm -bg black -fg yellow -geometry 200x30+0+0 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS Sequencer Controller" -e python $TS_OCS_SEQUENCER_SRC/OcsSequencerController.py &
