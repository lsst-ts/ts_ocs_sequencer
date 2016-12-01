#!/bin/sh

# +
# long form help behavioural command(s)
# -
for CMD in "" initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --help"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --help
done

# +
# short form help behavioural command(s)
# -
for CMD in "" initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD -h"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD -h
done

# +
# long form example behavioural command(s)
# -
for CMD in initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  if [ $CMD == "initGuiders" ]; then
    CMD="$CMD --roispec=roiData"
  elif [ $CMD == "initImage" ]; then
    CMD="$CMD --deltat=5.0"
  elif [ $CMD == "setFilter" ]; then
    CMD="$CMD --name=u"
  elif [ $CMD == "takeImages" ]; then
    CMD="$CMD --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=True --wfs=True --imagesequencename=$$"
  elif [ $CMD == "clear" ]; then
    CMD="$CMD --nclear=2"
  elif [ $CMD == "discardRows" ]; then
    CMD="$CMD --rows=2"
  elif [ $CMD == "startImage" ]; then
    CMD="$CMD --shutter=True --science=True --guide=True --wfs=True --imagesequencename=$$"
  fi
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True
done

# +
# short form example generic command(s)
# -
for CMD in initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  if [ $CMD == "initGuiders" ]; then
    CMD="$CMD -r=roiData"
  elif [ $CMD == "initImage" ]; then
    CMD="$CMD -d=5.0"
  elif [ $CMD == "setFilter" ]; then
    CMD="$CMD -n=u"
  elif [ $CMD == "takeImages" ]; then
    CMD="$CMD -n=2 -x=15.0 -u=True -c=True -g=True -w=True -i=$$"
  elif [ $CMD == "clear" ]; then
    CMD="$CMD -n=2"
  elif [ $CMD == "discardRows" ]; then
    CMD="$CMD -r=2"
  elif [ $CMD == "startImage" ]; then
    CMD="$CMD -u=True -c=True -g=True -w=True -i=$$"
  fi
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True
done

# +
# function for a commandable entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py "$@" --system=CCS --entity=Camera
}

# +
# long form help commands via function
# -
for CMD in "" initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  tput setaf 2
  echo "Executing> camera $CMD --help"
  tput setaf 4
  camera $CMD --help
done

# +
# short form help commands via function
# -
for CMD in "" initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  tput setaf 2
  echo "Executing> camera $CMD -h"
  tput setaf 4
  camera $CMD -h
done

# +
# long form example generic command(s) via function
# -
for CMD in initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  if [ $CMD == "initGuiders" ]; then
    CMD="$CMD --roispec=roiData"
  elif [ $CMD == "initImage" ]; then
    CMD="$CMD --deltat=5.0"
  elif [ $CMD == "setFilter" ]; then
    CMD="$CMD --name=u"
  elif [ $CMD == "takeImages" ]; then
    CMD="$CMD --numimages=2 --exptime=15.0 --shutter=True --science=True --guide=True --wfs=True --imagesequencename=$$"
  elif [ $CMD == "clear" ]; then
    CMD="$CMD --nclear=2"
  elif [ $CMD == "discardRows" ]; then
    CMD="$CMD --rows=2"
  elif [ $CMD == "startImage" ]; then
    CMD="$CMD --shutter=True --science=True --guide=True --wfs=True --imagesequencename=$$"
  fi
  tput setaf 2
  echo "Executing> camera $CMD --simulate=True"
  tput setaf 4
  camera $CMD --simulate=True
done

# +
# short form example generic command(s) via function
# -
for CMD in initGuiders initImage setFilter takeImages clear discardRows endImage startImage; do
  if [ $CMD == "initGuiders" ]; then
    CMD="$CMD -r=roiData"
  elif [ $CMD == "initImage" ]; then
    CMD="$CMD -d=5.0"
  elif [ $CMD == "setFilter" ]; then
    CMD="$CMD -n=u"
  elif [ $CMD == "takeImages" ]; then
    CMD="$CMD -n=2 -x=15.0 -u=True -c=True -g=True -w=True -i=$$"
  elif [ $CMD == "clear" ]; then
    CMD="$CMD -n=2"
  elif [ $CMD == "discardRows" ]; then
    CMD="$CMD -r=2"
  elif [ $CMD == "startImage" ]; then
    CMD="$CMD -u=True -c=True -g=True -w=True -i=$$"
  fi
  tput setaf 2
  echo "Executing> camea $CMD --simulate=True"
  tput setaf 4
  camera $CMD --simulate=True
done

tput setaf sgr0
