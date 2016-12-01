#!/bin/sh

# +
# function for a camera entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py "$@" --system=CCS --entity=Camera --simulate=False --timeout=15
}

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py entercontrol --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera entercontrol"
tput setaf 4
camera entercontrol

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py start --startid=Normal --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera start Normal"
tput setaf 4
camera start --startid=Normal

# python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py enable --system=CCS --entity=camera --simulate=False --timeout=15
tput setaf 2
echo "Executing> camera enable"
tput setaf 4
camera enable

tput setaf sgr0

