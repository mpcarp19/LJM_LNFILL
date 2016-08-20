from LNChannel import LNChannel
import time

configure = ['0','2','Test','1']
serialnums = ["470010276","470010916"]
chs = ['0','1','2','3','4','5','6','7','8','9','10','11']
go = True

for serialnum in serialnums:
  for ch in chs:
    configure[0] = ch
    LNCh=LNChannel(serialnum,configure)
    LNCh.info()
    isOpen = LNCh.T7Status()
    if isOpen:
      volt = LNCh.read_PT100()
      print "PT100 voltage ", volt
      LEDstate =  LNCh.LED_State()
      print "LED State ", LEDstate
      status = LNCh.close_valve()
      print "Valve is ",status
      #time.sleep( 5 )
      status = LNCh.open_valve()
      print "Valve is ",status
      time.sleep (5) 
      status = LNCh.close_valve()
      print "Valve is ", status 
      print "Valve was open for ",LNCh.time_open()," sec."
    else:
      print "T7 with serial #",serialnum," is not reachable"
      break
