#!/usr/bin/env python
from LNChannel import LNChannel
import time
import sys

valves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

serialnum="470010276"
print "Closing All Valves on A-Side"
for valve in valves:
  valveid = str(valve)
  configure = [valveid,'2','Valve','1']
  test=LNChannel(serialnum,configure)
  #test.info()
  isAlive = test.T7Status()
  if isAlive:
    status = test.close_valve()
    print "Valve ",valve," is ",status
  else:
    print "T7 with serial #",serialnum," is not reachable - Valve was not closed"

