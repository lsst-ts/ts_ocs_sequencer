========
CLI
========

python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py <command> [<args>]

 <command>::

	start - Configure the commandable entity        

	abort - Abort any running command in the commandable entity

	entercontrol - Take control of the commandable entity  

	standby - Unconfigure the commandable entity      

	stop - Stop any running command in the commandable entity

	enable - Enable the commandable entity           

	exitcontrol - Relinquish control of the commandable entity

	disable - Disable the commandable entity          

	setvalue - Set a parameter to a given value in the commandable entity

 [<args>]::

  -h, --help  show this help message and exit


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py abort [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  abort - Abort any running command in the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py disable [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  disable - Disable the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py enable [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  enable - Enable the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py enterControl [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  enterControl - Take control of the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py exitControl [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  exitControl - Relinquish control of the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py setValue [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-p PARAMETER] [-v VALUE]

 <command>::

  setValue - Set a parameter to a given value in the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -p PARAMETER, --parameter PARAMETER
                        parameter name
  -v VALUE, --value VALUE
                        string-encoded value


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py standby [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  standby - Unconfigure the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py start [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-i STARTID]

 <command>::

  start - Configure the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -i STARTID, --startid STARTID
                        configuration identifier


python $TS_OCS_SEQUENCER_SRC/OcsGenericEntityCli.py stop [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-d DEVICE]

 <command>::

  stop - Stop any running command in the commandable entity

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -d DEVICE, --device DEVICE
                        device identifier


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py <command> [<args>]

 <command>::

	start - Configure the commandable entity        
	abort - Abort any running command in the commandable entity
	entercontrol - Take control of the commandable entity  
	standby- Unconfigure the commandable entity      
	stop - Stop any running command in the commandable entity
	enable - Enable the commandable entity           
	exitcontrol - Relinquish control of the commandable entity
	disable - Disable the commandable entity          
	setvalue - Set a parameter to a given value in the commandable entity

	clear - Clear the focal plane                   
	discardRows - Discard a number of rows within each image whilst integrating
	endImage - Terminate open-ended image acquisition  
	initGuiders - Initialize the guiders                  
	initImage - Initialize the image acquisition        
	startImage - Open-ended start image acquisition      
	setFilter - Set filter into beam                    
	takeImages - Take a number of exposures              

 [<args>]::

  -h, --help  show this help message and exit


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py clear [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-n NCLEAR]

 <command>::

  clear - Clears the focal plane a given number of times

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -n NCLEAR, --nclear NCLEAR
                        number of clears


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py discardRows [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-r ROWS]

 <command>::

  discardRows - discard a given number of rows during an open-ended startImage() command

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -r ROWS, --rows ROWS  number of rows


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py endImage [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT]

 <command>::

  endImage - terminate a startImage() command

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py initGuiders [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-r ROISPEC]

 <command>::

  initGuiders - initialize the guiders according to given specification

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -r ROISPEC, --roispec ROISPEC
                        region-of-interest specification


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py initImage [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-d DELTAT]

 <command>::

  initImage - initialize the image acquisition with an estimated delta time until the shutter opens

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -d DELTAT, --deltat DELTAT
                        delta time


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py setFilter [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-n NAME]

 <command>::

  setFilter - set to a filter with the given name

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -n NAME, --name NAME  filter name


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py startImage [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-u SHUTTER] [-c SCIENCE] [-g GUIDE] [-w WFS] [-i IMAGESEQUENCENAME]

 <command>::

  startImage - start an open-ended image acquisition

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -u SHUTTER, --shutter SHUTTER
                        shutter state
  -c SCIENCE, --science SCIENCE
                        science area state
  -g GUIDE, --guide GUIDE
                        guider state
  -w WFS, --wfs WFS     wavefront sensor state
  -i IMAGESEQUENCENAME, --imagesequencename IMAGESEQUENCENAME
                        image sequence name


python $TS_OCS_SEQUENCER_SRC/OcsCameraEntityCli.py takeImages [-h] [-s SYSTEM] [-e ENTITY] [-m SIMULATE] [-t TIMEOUT] [-n NUMIMAGES] [-x EXPTIME] [-u SHUTTER] [-c SCIENCE] [-g GUIDE] [-w WFS] [-i IMAGESEQUENCENAME]

 <command>::

  takeImages - take a given number of images with the parameters selected

 [<args>]::

  -h, --help            show this help message and exit
  -s SYSTEM, --system SYSTEM
                        principal subsystem
  -e ENTITY, --entity ENTITY
                        commandable entity
  -m SIMULATE, --simulate SIMULATE
                        set entity to simulate mode
  -t TIMEOUT, --timeout TIMEOUT
                        set entity to simulate mode
  -n NUMIMAGES, --numimages NUMIMAGES
                        number of exposures
  -x EXPTIME, --exptime EXPTIME
                        exposure time
  -u SHUTTER, --shutter SHUTTER
                        shutter state
  -c SCIENCE, --science SCIENCE
                        science area state
  -g GUIDE, --guide GUIDE
                        guider state
  -w WFS, --wfs WFS     wavefront sensor state
  -i IMAGESEQUENCENAME, --imagesequencename IMAGESEQUENCENAME
                        image sequence name
