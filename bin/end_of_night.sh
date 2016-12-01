#!/bin/sh

# +
# function for a camera entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py "$@" --system=CCS --entity=Camera --simulate=False --timeout=15
}

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py disable --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera disable"
tput setaf 4
camera disable

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py standby --startid=Normal --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera standby"
tput setaf 4
camera standby

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py exitcontrol --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera exitcontrol"
tput setaf 4
camera exitcontrol

tput setaf sgr0

