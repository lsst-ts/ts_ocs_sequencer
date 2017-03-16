#!/bin/sh

xterm -bg black -fg green -geometry 200x30+0+0 -xrm 'XTerm.vt100.allowTitleOps: false' -T "OCS Sequencer Events" -e python $TS_OCS_SEQUENCER_BIN/logevent_sequencer_threadclass.py Sequencer &
