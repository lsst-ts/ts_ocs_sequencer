#!/bin/sh

. setup.env.sh

python -m pytest $TS_OCS_SEQUENCER_TESTS/test_OcsGenericEntityCli.py
python -m pytest $TS_OCS_SEQUENCER_TESTS/test_OcsGenericEntity.py
python -m pytest $TS_OCS_SEQUENCER_TESTS/test_OcsCameraEntityCli.py
python -m pytest $TS_OCS_SEQUENCER_TESTS/test_OcsCameraEntity.py
