========
API
========

OcsGenericEntity.py::

  OcsGenericEntity(system='', entity='', simulate=True)
    - returns an object representing the (generic) commandable entity, or None
  Methods:
    abort()
      - execute a generic abort() command
    disable()
      - execute a generic disable() command
    enable()
      - execute a generic enable() command
    enterControl()
      - execute a generic enterControl() command
    exitControl()
      - execute a generic exitControl() command
    setValue(parameter='', value='')
      - execute a generic setValue() command, arguments are the parameter name and string-encoded value
    standby()
      - execute a generic standby() command
    start(startid='')
      - execute a generic start() command, arguments are the startid
    stop(device='')
      - execute a generic stop() command, arguments are the device name

OcsGenericEntityCli.py::

  OcsGenericEntityCli()
    - returns an object representing the (generic) commandable entity command line, or None
  Methods:
    execute()
      - execute the parser and return a dictionary of command line objects

OcsCameraEntity.py::

  OcsCameraEntity(system='CCS', entity='Camera', simulate=True)
    - returns an object representing the camera commandable entity, or None
  Methods:
    abort()
      - execute a generic abort() command
    disable()
      - execute a generic disable() command
    enable()
      - execute a generic enable() command
    enterControl()
      - execute a generic enterControl() command
    exitControl()
      - execute a generic exitControl() command
    setValue(parameter='', value='')
      - execute a generic setValue() command, arguments are the parameter name and string-encoded value
    standby()
      - execute a generic standby() command
    start(startid='')
      - execute a generic start() command, arguments are the startid
    stop(device='')
      - execute a generic stop() command, arguments are the device name
    clear(nclear=0)
      - executes a behavioural clear() command, arguments are the number of clears to perform
    discardRows(rows=0)
      - executes a behavioural discardRows() command, arguments are the number of rows to discard
    endImage()
      - executes a behavioural endImage() command
    initGuiders(roiSpec='')
      - executes a behavioural initGuiders() command, arguments are the roi-specification
    initImage(deltaT=0.0)
      - executes a behavioural initImage() command, arguments are the delta time before the shutter opens
    startImage()
      - executes a behavioural startImage() command, arguments are the image name
    startImage(shutter=True, science=True, guide=True, wfs=True, ImageSequenceName='')
      - executes a behavioural takeImages() command, arguments are the the shutter condition (True=Open), 
        the science array enabled, guider enabled, wavefront sending enabled and the image sequence name.
        This command terminates via the endImage() command
    takeImages(numImages=0, expTime=0.0, shutter=True, science=True, guide=True, wfs=True, ImageSequenceName='')
      - executes a behavioural takeImages() command, arguments are the number of images to take, the exposure time
        for each image, the shutter condition (True=Open), the science array enabled, guider enabled, wavefront
        sending enabled and the image sequence name

OcsCameraEntityCli.py::

  OcsCameraEntityCli()
    - returns an object representing the camera commandable entity command line, or None
  Methods:
    execute()
      - execute the parser and return a dictionary of command line objects
