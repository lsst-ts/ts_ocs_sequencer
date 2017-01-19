#!/bin/sh

# +
# function for a camera entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py "$@" --system=CCS --entity=Camera --simulate=False
}

tput setaf 2
echo "Executing> camera disable"
tput setaf 4
camera disable >> /dev/null 2>&1

tput setaf 2
echo "Executing> camera standby"
tput setaf 4
camera standby >> /dev/null 2>&1

tput setaf 2
echo "Executing> camera exitcontrol"
tput setaf 4
camera exitcontrol >> /dev/null 2>&1

tput setaf sgr0
