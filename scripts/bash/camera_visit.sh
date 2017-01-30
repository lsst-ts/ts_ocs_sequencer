#!/bin/sh

# +
# function for a camera entity
# -

camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py "$@" --system=CCS --entity=Camera --simulate=False
}

tput setaf 2
echo "Executing> camera setfilter --name='g-9' --timeout=60"
tput setaf 4
camera setfilter --name='g-9' --timeout=60 >> /dev/null 2>&1

tput setaf 2
echo "Executing> camera initimage --deltat=4.0 --timeout=10"
tput setaf 4
camera initimage --deltat=4.0 --timeout=10 >> /dev/null 2>&1

tput setaf 2
isn=`python $TS_OCS_COMMON_SRC/ocs_id.py --ascii`
echo "Executing> camera takeimages --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=False --wfs=False --imagesequencename=$isn --timeout=45"
tput setaf 4
camera takeimages --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=False --wfs=False --imagesequencename=$isn --timeout=45 >> /dev/null 2>&1

tput setaf sgr0
