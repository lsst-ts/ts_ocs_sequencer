#!/bin/sh

# +
# function for a sequencer entity
# -
sequencer () {
  python $TS_OCS_SEQUENCER_SRC/OcsSequencerEntityCli.py "$@" --system=OCS --entity=ocs --simulate=False
}

tput setaf 2
echo "Executing> sequencer entercontrol"
tput setaf 4
sequencer entercontrol >> /dev/null 2>&1

startid="${1:-Normal}"
tput setaf 2
echo "Executing> sequencer start --startid=$startid"
tput setaf 4
sequencer start --startid=$startid >> /dev/null 2>&1

tput setaf 2
echo "Executing> sequencer enable"
tput setaf 4
sequencer enable >> /dev/null 2>&1

tput setaf sgr0
