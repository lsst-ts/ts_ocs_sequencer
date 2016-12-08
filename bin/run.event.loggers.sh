#!/bin/sh

xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsEntityStartup  -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityStartup.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsEntityShutdown -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityShutdown.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsCommandIssued  -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandIssued.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsCommandStatus  -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandStatus.py &
