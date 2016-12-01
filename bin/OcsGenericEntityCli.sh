#!/bin/sh

# +
# long form help generic command(s)
# -
for CMD in "" abort disable enable enterControl exitControl setValue standby start stop; do
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD --help"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD --help
done

# +
# short form help generic command(s)
# -
for CMD in "" abort disable enable enterControl exitControl setValue standby start stop; do
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD -h"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD -h
done

# +
# long form example generic command(s)
# -
for CMD in abort disable enable enterControl exitControl setValue standby start stop; do
  if [ $CMD == "setValue" ]; then
    CMD="$CMD --parameter=MyParameter --value=MyValue"
  elif [ $CMD == "start" ]; then
    CMD="$CMD --startid=Normal"
  elif [ $CMD == "stop" ]; then
    CMD="$CMD --device=Camera"
  fi
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD --system=CCS --entity=Camera --simulate=True
done

# +
# short form example generic command(s)
# -
for CMD in abort disable enable enterControl exitControl setValue standby start stop; do
  if [ $CMD == "setValue" ]; then
    CMD="$CMD -p=MyParameter -v=MyValue"
  elif [ $CMD == "start" ]; then
    CMD="$CMD -i=Normal"
  elif [ $CMD == "stop" ]; then
    CMD="$CMD -d=Camera"
  fi
  tput setaf 2
  echo "Executing> python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD -s=CCS -e=Camera -m=True"
  tput setaf 4
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py $CMD -s=CCS -e=Camera -m=True
done

# +
# function for a commandable entity
# -
camera () {
  python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py "$@" --system=CCS --entity=Camera
}

# +
# long form help commands via function
# -
for CMD in "" abort disable enable enterControl exitControl setValue standby start stop; do
  tput setaf 2
  echo "Executing> camera $CMD --help"
  tput setaf 4
  camera $CMD --help
done

# +
# short form help commands via function
# -
for CMD in "" abort disable enable enterControl exitControl setValue standby start stop; do
  tput setaf 2
  echo "Executing> camera $CMD -h"
  tput setaf 4
  camera $CMD -h
done

# +
# long form example generic command(s) via function
# -
for CMD in abort disable enable enterControl exitControl setValue standby start stop; do
  if [ $CMD == "setValue" ]; then
    CMD="$CMD --parameter=MyParameter --value=MyValue"
  elif [ $CMD == "start" ]; then
    CMD="$CMD --startid=Normal"
  elif [ $CMD == "stop" ]; then
    CMD="$CMD --device=Camera"
  fi
  tput setaf 2
  echo "Executing> camera $CMD --simulate=True"
  tput setaf 4
  camera $CMD --simulate=True
done

# +
# short form example generic command(s) via function
# -
for CMD in abort disable enable enterControl exitControl setValue standby start stop; do
  if [ $CMD == "setValue" ]; then
    CMD="$CMD -p=MyParameter -v=MyValue"
  elif [ $CMD == "start" ]; then
    CMD="$CMD -i=Normal"
  elif [ $CMD == "stop" ]; then
    CMD="$CMD -d=Camera"
  fi
  tput setaf 2
  echo "Executing> camera $CMD -m=True"
  tput setaf 4
  camera $CMD -m=True
done

tput setaf sgr0
