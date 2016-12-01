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
camera entercontrol

tput setaf 2
echo "Executing> camera start --startid=Normal"
tput setaf 4
camera start --startid=Normal

tput setaf 2
echo "Executing> camera enable"
tput setaf 4
camera enable

tput setaf 2
echo "Executing> camera setfilter --name='g-9' --timeout=60"
tput setaf 4
camera setfilter --name='g-9' --timeout=60

tput setaf 2
echo "Executing> camera initimage --deltat=10.5 --timeout=5"
tput setaf 4
camera initimage --deltat=10.5 --timeout=5

tput setaf 2
echo "Executing> camera takeimages --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=False --wfs=False --imagesequencename=$$ --timeout=40"
tput setaf 4
camera takeimages --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=False --wfs=False --imagesequencename=$$ --timeout=40

tput setaf 2
echo "Executing> camera initguiders --roiSpec='1,1,1,1 100,100,100,100 32,32,32,32' --timeout=5"
tput setaf 4
camera initguiders --roispec='1,1,1,1 100,100,100,100 32,32,32,32' --timeout=5

tput setaf 2
echo "Executing> camera disable"
tput setaf 4
camera disable

tput setaf 2
echo "Executing> camera standby"
tput setaf 4
camera standby

tput setaf 2
echo "Executing> camera exitcontrol"
tput setaf 4
camera exitcontrol

tput setaf sgr0
