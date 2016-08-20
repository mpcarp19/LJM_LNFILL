#!/usr/bin/env python
from LNChannel import LNChannel
import sys
import time

Manifolds = []
Vents = []
Detectors = []
enabledDets = []

def main():

# This method will do the main processing

  if len(sys.argv) < 2:
    print "command: LNFill.py configfile"
    return

  #configfile = "T7-470010276.config"
  configfile = str(sys.argv[1])
  status = setupConfig(configfile)
  if status == 1:
    "Setup failed - check configuratoin file."
    return

# All looks good - continue

  print "Number of Manifolds configured ", len(Manifolds)
  print "Number of Vents configured ",len(Vents)
  print "Number of Detectors configured ", len(Detectors)

# Check # of Manifolds
  isMani = False
  if len(Manifolds) > 1:
    print "# Manifolds > 1 - cannot process fill."
    return  
  elif len(Manifolds) == 1:
    Manifold = Manifolds[0]
    begin_fill_time = Manifold.get_tstamp()
    if Manifold.is_enabled() == 1: isMani = True
    if Manifold.T7Status() == 0:
      print "T7 with serial #", Manifold.get_serialnum() ," is not reachable - FILL ABORTED"
      #return

# Check # of Vents

  isVent = False
  if len(Vents) > 1:
    print "# Vents > 1 - cannot process fill."
    return  
  elif len(Vents) == 1:
    Vent = Vents[0]
    begin_fill_time = Vent.get_tstamp()
    if Vent.is_enabled() == 1: isVent = True
    if Vent.T7Status() == 0:
      print "T7 with serial #", Vent.get_serialnum() ," is not reachable - FILL ABORTED"
      #return

# Check # of Detectors 

  numEnDets = 0
  if len(Detectors) > 0:
    if Detectors[0].T7Status() == 0:
      print "T7 with serial #", Detectors[0].get_serialnum() ," is not reachable - FILL ABORTED"
      #return
    index = 0
    for det in Detectors:
      begin_fill_time = det.get_tstamp()
      if det.is_enabled()==1: 
        numEnDets = numEnDets+1
        enabledDets.append(index)
      index = index + 1

# summarized what is enabled and ready to fill

  print "Number of Enabled Manifolds ", int(isMani)
  print "Number of Enabled Vents ", int(isVent)
  print "Number of Enabled Detectors found ", numEnDets
     
# Final check - do we have at least one detector or vent enabled 

  if isVent==False & numEnDets == 0:
    print "No vents or detectors enabled - Nothing to do - FILL ABORTED."
    return

# Looks like we can try a fill - first open mainfold

  if isMani: status = Manifold.open_valve()

# Now open Vent and keep open until its LED goes high

  if isVent:
    status = Vent.open_valve()
    print "Opening Vent Valve: status = ",status
    while Vent.LED_State() == 0:
      time.sleep(5)
    status = Vent.close_valve()
    end_fill_time = Vent.get_tstamp()
    print "Clasing Vent Valve: status =",status," Fill time = ",Vent.time_open()

# Now Lets fill enabled detectors

  if numEnDets > 0:
    for i in enabledDets:
      det = Detectors[i]
      status = det.open_valve()
      temp = det.read_PT100()
      print "Filling ",det.get_name(),"- Open Valve ",det.get_valve(),"- PT100 at ",temp," Volts"
    allclosed = False
    while not allclosed:
      numopen = 0
      for i in enabledDets:
        det = Detectors[i]
        if (det.isVOpen() == 1) and (det.LED_State() == 1):
          status = det.close_valve()
          end_fill_time = det.get_tstamp()
          print det.get_name()," is filled - Fill Time = ",det.time_open(),"Valve ",det.get_valve()," closed"
        elif det.isVOpen() == 1:
          numopen = numopen+1
      if numopen == 0 :
        allclosed = True
      else:
        time.sleep(5)

# Last thing is to close Manifold valve if enabled
  if isMani: 
    status = Manifold.close_valve()
    end_fill_time = Manifold.get_tstamp()

# Report Total Fill time
  fill_time = end_fill_time - begin_fill_time
  print "Fill is finished - Time of fill was ", fill_time, " sec"

# read config file and creat LNChannel opject based on type
def setupConfig(configfile):
  file = configfile
  status = 0
  try:
    config = open(file,"r")
  except Exception as e:  # figure out what exception 
     status = 1
     return status

  content = config.readlines() 

  # parse content
  for line in content:
     if line.startswith("#Serial"):
       serialnum = line.split("=")[1].strip()
       print "Serial Number is ",serialnum
     elif line.startswith("#Config"):
       configure=1
     elif line.startswith("#"):
       ncommet=0
     elif configure==1:
       results = line.split(",")
       if len(results) == 4:
         i = 0
         for result in results:  
           results[i] = result.strip()
           i=i+1
         # divide by type
         if int(results[1]) == 0:
           Manifolds.append(LNChannel(serialnum,results))
         elif int(results[1]) == 1:
	   Vents.append(LNChannel(serialnum,results))
         elif int(results[1]) == 2:
 	   Detectors.append(LNChannel(serialnum,results))

  return status
# Now run main
main()

