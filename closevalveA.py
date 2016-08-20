#!/usr/bin/env python
from LNChannel import LNChannel
import time
import sys

if len(sys.argv) < 2:
  print "command: closevalveA.py valvenum"
  quit()

valve = int(sys.argv[1])

if(valve < 1) or (valve>12):
  print "Valid valve #'s are from 1 to 12"
  quit()

valveid = str(valve)
configure = [valveid,'2','Valve','1']
serialnum="470010276"

test=LNChannel(serialnum,configure)
#test.info()
isAlive = test.T7Status()
if isAlive:
  status = test.close_valve()
  print "Valve ",valve," is ",status
else:
  print "T7 with serial #",serialnum," is not reachable - Valve was not opened"

