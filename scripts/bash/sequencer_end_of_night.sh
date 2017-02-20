#!/bin/sh

# +
# function for a sequencer entity
# -
sequencer () {
  python $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py "$@" --system=OCS --entity=ocs --simulate=False
}

tput setaf 2
echo "Executing> sequencer disable"
tput setaf 4
sequencer disable >> /dev/null 2>&1

tput setaf 2
echo "Executing> sequencer standby"
tput setaf 4
sequencer standby >> /dev/null 2>&1

tput setaf 2
echo "Executing> sequencer exitcontrol"
tput setaf 4
sequencer exitcontrol >> /dev/null 2>&1

tput setaf sgr0
