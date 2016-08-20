from LNChannel import LNChannel
import time

  if len(sys.argv) < 2:
    print "command: LNFill.py configfile"
    return


configure = ['1','2','Test','1']
serialnum="470010276"



test=LNChannel(serialnum,configure)
test.info()
isOpen = test.T7Status()
if isOpen:
  print "PT100 voltage ", test.read_PT100()
  print "LED State ", test.LED_State()
  status = test.close_valve()
  print "Valve is ",status
  time.sleep( 5 )
  status = test.open_valve()
  print "Valve is ",status
  time.sleep (5) 
  status = test.close_valve()
  print "Valve is ", status 
else:
  print "T7 with serial #",serialnum," is not reachable"
