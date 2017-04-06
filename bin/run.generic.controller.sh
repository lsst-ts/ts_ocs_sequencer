#!/bin/sh

arg1="${1:-Sequencer}"

xterm -bg black -fg yellow -geometry 200x30+0+0 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS ${arg1} Controller" -e python $TS_OCS_SEQUENCER_SRC/OcsGenericController.py ${arg1} &
