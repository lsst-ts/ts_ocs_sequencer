#!/bin/sh

arg1="${1:-_ocs}"

# if no command line arguments, start the event logger for all events
if [[ $# -eq 0 ]]; then
  xterm -bg black -fg green -geometry 200x30+0+0 -xrm 'XTerm.vt100.allowTitleOps: false' -132 -T "Event Logger" -e python $TS_OCS_SEQUENCER_BIN/logevent${arg1}.py &

# start a specific event logger
else
  while [[ $# -gt 0 ]]; do
    case $1 in
      ocs_logevent_ocsEntityShutdown | logevent_ocsEntityShutdown | ocsEntityShutdown )
        xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsEntityShutdown -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityShutdown.py &
        ;;
      ocs_logevent_ocsEntityStartup | logevent_ocsEntityStartup | ocsEntityStartup )
        xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsEntityStartup -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntityStartup.py &
        ;;
      ocs_logevent_ocsEntitySummaryState | logevent_ocsEntitySummaryState | ocsEntitySummaryState )
        xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsEntitySummaryState -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsEntitySummaryState.py &
        ;;
      ocs_logevent_ocsCommandIssued | logevent_ocsCommandIssued | ocsCommandIssued )
        xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsCommandIssued -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandIssued.py &
        ;;
      ocs_logevent_ocsCommandStatus | logevent_ocsCommandStatus | ocsCommandStatus )
        xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T logevent_ocsCommandStatus -e python $TS_OCS_SEQUENCER_BIN/logevent_ocsCommandStatus.py &
        ;;
    esac
    shift
  done
fi
