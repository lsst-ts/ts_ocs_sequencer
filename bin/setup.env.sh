#!/bin/sh

# +
# set the default path below
# -
export TS_OCS_SEQUENCER_PATH=/usr/local/ts_ocs_sequencer

# +
# set derived environmental variable(s)
# -
export TS_OCS_SEQUENCER_BIN=${TS_OCS_SEQUENCER_PATH}/bin
export TS_OCS_SEQUENCER_CONF=${TS_OCS_SEQUENCER_PATH}/conf
export TS_OCS_SEQUENCER_DOCS=${TS_OCS_SEQUENCER_PATH}/docs
export TS_OCS_SEQUENCER_LOG=${TS_OCS_SEQUENCER_PATH}/log
export TS_OCS_SEQUENCER_SRC=${TS_OCS_SEQUENCER_PATH}/ts_ocs_sequencer
export TS_OCS_SEQUENCER_TESTS=${TS_OCS_SEQUENCER_PATH}/tests

# +
# adjust PATH and PYTHONPATH
# -
export PATH=${PATH}:${TS_OCS_SEQUENCER_BIN}:${TS_OCS_SEQUENCER_SRC}
export PYTHONPATH=${PYTHONPATH}:${TS_OCS_SEQUENCER_SRC}
export PYTHONPATH=${PYTHONPATH}:/usr/local/ts_sal/lib