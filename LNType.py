
import Constants

class Detector:

   ''' Create a Detector object - associates a Valve, PT100 and LED to it'''

   def __init__(self, sn,configure):

     self.serialnum = sn.strip()
     self.ch = int(configure[0]);
     self.type = int(configure[1]);
     self.name = configure[2];
     self.enabled = int(configure[3]);
     self.valve = Constants.Valves[self.ch]
     self.PT100 = Constants.PT100s[self.ch]
     self.LED   = Constants.LEDs[self.ch]

   # print information
   def info(self):
     print("%s is attached to T7 %s. Ch = %i, Type = %i, Enabled = %i, Valve = %s, PT100 = %s, LED= %s \n" % \
               (self.name,self.serialnum,self.ch,self.type,self.enabled,self.valve,self.PT100,self.LED))

   # read PT100 and return (temp,volt)???
   def read_PT100(self)
     try:
       handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     except:
       return -1
     voltage = ljm.eReadName(handle, self.PT100)
     ljm.close(handle)
     return voltage
   
   # read state of LED
   def LED_State(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     state = ljm.eReadName(handle, self.LED)
     ljm.close(handle)
     return state

   # open valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     OPEN=1
     self.timeATopen = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,OPEN)
     ljm.close(handle)
     return OPEN

   # close valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     CLOSE=0
     self.timeATclose = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,CLOSE)
     ljm.close(handle)
     return CLOSE

   # time valve was opened
   def time_opened(self)
     return self.timeATclose - self.timeATopen

class Manifold:

   ''' Creat a Manifold object - associates only a Valve to it'''

   def __init__(self, sn,configure):

     self.serialnum = sn.strip()
     self.ch = int(configure[0]);
     self.type = int(configure[1]);
     self.name = configure[2];
     self.enabled = int(configure[3]);
     self.valve = Constants.Valves[self.ch]
     self.PT100 = "null"
     self.LED   = "null"

   # print information
   def info(self):
     print("%s is attached to T7 %s. Ch = %i, Type = %i, Enabled = %i, Valve = %s, PT100 = %s, LED= %s \n"% \
                (self.name,self.serialnum,self.ch,self.type,self.enabled,self.valve,self.PT100,self.LED))

   # open valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     OPEN=1
     self.timeATopen = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,OPEN)
     ljm.close(handle)
     return OPEN

   # close valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     CLOSE=0
     self.timeATclose = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,CLOSE)
     ljm.close(handle)
     return CLOSE

   # time valve was opened
   def time_opened(self)
     return self.timeATclose - self.timeATopen


class Vent:

   ''' Creat a Manifold object - associates  a Vavle adnd LED to it'''

   def __init__(self, sn, configure):

     self.serialnum = sn.strip()
     self.ch = int(configure[0]);
     self.type = int(configure[1]);
     self.name = configure[2];
     self.enabled = int(configure[3]);
     self.valve = Constants.Valves[self.ch]
     self.PT100 = "null"
     self.LED   = Constants.LEDs[self.ch]

   # print information
   def info(self):
     print("%s is attached to T7 %s. Ch = %i, Type = %i, Enabled = %i, Valve = %s, PT100 = %s, LED= %s \n" % \
                (self.name,self.serialnum,self.ch,self.type,self.enabled,self.valve,self.PT100,self.LED))

   # read state of LED
   def LED_State(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     state = ljm.eReadName(handle, self.LED)
     ljm.close(handle)
     return state

   # open valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     OPEN=1
     self.timeATopen = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,OPEN)
     ljm.close(handle)
     return OPEN

   # close valve
   def open_valve(self)
     handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET,self.serialnum)
     CLOSE=0
     self.timeATclose = ljm.eReadName(handle,"RTC_TIME_S")
     ljm.eWriteNames(handle, self.valve,CLOSE)
     ljm.close(handle)
     return CLOSE

   # time valve was opened
   def time_opened(self)
     return self.timeATclose - self.timeATopen

