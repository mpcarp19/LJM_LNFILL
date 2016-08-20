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

  #print "Number of Manifolds configured ", len(Manifolds)
  #print "Number of Vents configured ",len(Vents)
  print "Number of Detectors configured ", len(Detectors)

# Check # of Detectors 

  numEnDets = 0
  if len(Detectors) > 0:
    if Detectors[0].T7Status() == 0:
      print "T7 with serial #", Detectors[0].get_serialnum() ," is not reachable - Quitting"
      return
    index = 0
    for det in Detectors:
      begin_fill_time = det.get_tstamp()
      if det.is_enabled()==1: 
        numEnDets = numEnDets+1
        enabledDets.append(index)
      index = index + 1

# summarized what is enabled and ready to fill

  #print "Number of Enabled Manifolds ", int(isMani)
  #print "Number of Enabled Vents ", int(isVent)
  print "Number of Enabled Detectors found ", numEnDets
     
# Now Lets get Temps

  if numEnDets > 0:
    for i in enabledDets:
      det = Detectors[i]
      temp = det.read_PT100()
      print "Temp. for ",det.get_name()," is at ",temp," Volts"

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

