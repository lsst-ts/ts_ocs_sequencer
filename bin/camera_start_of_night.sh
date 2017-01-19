#!/bin/sh

# +
# function for a camera entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py "$@" --system=CCS --entity=Camera --simulate=False
}

tput setaf 2
echo "Executing> camera entercontrol"
tput setaf 4
camera entercontrol >> /dev/null 2>&1

tput setaf 2
echo "Executing> camera start --startid=Normal"
tput setaf 4
camera start --startid=Normal >> /dev/null 2>&1

tput setaf 2
echo "Executing> camera enable"
tput setaf 4
camera enable >> /dev/null 2>&1

tput setaf sgr0
