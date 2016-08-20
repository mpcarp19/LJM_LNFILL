#!/usr/bin/env python
from labjack import ljm
from LNChannel2 import LNChannel2
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

# open and process the config file

  #configfile = "T7-470010276.config"
  configfile = str(sys.argv[1])
  status = setupConfig(configfile)
  if status == 1:
    print "Setup failed - Aborting"
    return
  serialnum =  # if all ok - setupConfig returns serial number of T7

# Now open up logfile 

date = time.localtime(time.time())
datestr = time.strftime("%Y%m%d.%H%M",date)
if serialnum.endswith("276"): 
  logfile="FillA."+datestr+".LOG"
elif serialnum.endswith("916"):
  logfile = "FillB."+datestr+".LOG"
else:
  logfile = "Fill."+datestr+".LOG"

#print logfile
f = open(logfile,"w")
loggit(f,"Fill Log")

# All looks good - continue
  loggit(f, "Number of Manifolds configured " + str(len(Manifolds)) )
  loggit(f, "Number of Vents configured ",  + str(len(Vents)) )
  loggit(f, "Number of Detectors configured " + str(len(Detectors)) )

# Check # of Manifolds
  isMani = False
  if len(Manifolds) > 1:
    loggit(f, "# Manifolds > 1 - cannot process fill.")
    return  
  elif len(Manifolds) == 1:
    Manifold = Manifolds[0]
    begin_fill_time = Manifold.get_tstamp()
    if Manifold.is_enabled() == 1: isMani = True

# Check # of Vents

  isVent = False
  if len(Vents) > 1:
    loggit(f, "# Vents > 1 - cannot process fill.")
    return  
  elif len(Vents) == 1:
    Vent = Vents[0]
    begin_fill_time = Vent.get_tstamp()
    if Vent.is_enabled() == 1: isVent = True

# Check # of Detectors 

  numEnDets = 0
  if len(Detectors) > 0:
    index = 0
    for det in Detectors:
      begin_fill_time = det.get_tstamp()
      if det.is_enabled()==1: 
        numEnDets = numEnDets+1
        enabledDets.append(index)
      index = index + 1

# summarized what is enabled and ready to fill

  loggit(f, "Number of Enabled Detectors configured " + str(numEnDets) )
     
# Final check - do we have at least one detector or vent enabled 

  if isVent==False and numEnDets == 0:
    loggit(f,"No vents or detectors enabled - Nothing to do - FILL ABORTED.")
    return

# timestamp start of fill

  localtime = time.asctime( time.localtime(time.time()) )
  logstr = "Fill beginning at ",localtime
  loggit(f,logstr)

# Looks like we can try a fill - first open mainfold

  if isMani: status = Manifold.open_valve()

# Now open Vent and keep open until its LED goes high

  if isVent:
    status = Vent.open_valve()
    loggit(f,"Opening Vent Valve: status = "+status)
    while Vent.LED_State() == 0:
      time.sleep(5)
    status = Vent.close_valve()
    end_fill_time = Vent.get_tstamp()
    loggit(f, "Clasing Vent Valve: status ="+status+" Fill time = "+str(int(Vent.time_open()+1)) )

# Now Lets fill enabled detectors

  if numEnDets > 0:
    for i in enabledDets:
      det = Detectors[i]
      status = det.open_valve()
      temp = det.read_PT100()
      stemp = "%.5f" % temp
      loggit(f, "Filling " + det.get_name() + "- Open Valve " + str(det.get_valve()) + "- PT100 at " + temp + " Volts")
    allclosed = False
    while not allclosed:
      numopen = 0
      for i in enabledDets:
        det = Detectors[i]
        if (det.isVOpen() == 1) and (det.LED_State() == 1):
          status = det.close_valve()
          end_fill_time = det.get_tstamp()
          otime = "%.1f" % det.time_open()
          loggit(f, det.get_name()+" is filled - Fill Time = " + otime + "Valve " + str(det.get_valve()) + " closed"
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
  fill_time = "%.1f" % end_fill_time - begin_fill_time
  loggit(f,"Fill is finished - Time of fill was " + fill_time + " sec"

# read config file and creat LNChannel opject based on type
def setupConfig(configfile):
  file = configfile
  status = 0
  try:
    config = open(file,"r")
  except Exception as e:  # figure out what exception 
     status = 1
     print "Could not find configuration file - Please check file name."
     return status

  content = config.readlines() 

  # parse content
  for line in content:
     if line.startswith("#Serial"):
       serialnum = line.split("=")[1].strip()
       print "Serial Number is ",serialnum
       # now open the labjack
       try:
         handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,serialnum)
       except ljm.LJMError as e:
         print e
         print "T7 with serial #",serialnum," is not reachable - FILL ABORTED"
         status = 1
         return status
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
           Manifolds.append(LNChannel2(handle,results))
         elif int(results[1]) == 1:
	   Vents.append(LNChannel2(handle,results))
         elif int(results[1]) == 2:
 	   Detectors.append(LNChannel2(handle,results))

  return serialnum

# logger routine prints to file and screen
def loggit(f,logstr):	
  print logstr
  f.write(logstr + "\n")
  return
# Now run main
main()

