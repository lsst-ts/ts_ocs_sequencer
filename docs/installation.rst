============
Installation
============

If the code tree is installed in /usr/local/ts_ocs_sequencer (for example), do this::

  1. Edit /usr/local/ts_ocs_sequencer/bin/setup.env.sh and set the root environmental variable:

       export TS_OCS_COMMON_PATH=/usr/local/ts_ocs_sequencer

  2. Place the following in ~/.bashrc, ~/.profile, /etc/bashrc or /etc/profile:

       if [ -f /usr/local/ts_ocs_sequencer/bin/setup.env.sh ]; then
         . /usr/local/ts_ocs_sequencer/bin/setup.env.sh
       fi
