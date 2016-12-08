#!/bin/sh

xterm -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityStartup.py &

xterm -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityShutdown.py &

xterm -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandIssued.py &

xterm -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandStatus.py &
