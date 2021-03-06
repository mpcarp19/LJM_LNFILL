from labjack import ljm
import Constants
import time

class LNChannel2:

   ''' Create an LNChannel object - associate a Valve, PT100 and LED to it
       This version requires the labjack to opened by the calling routine which
       passes the handle to the LNChannel object
   '''

   def __init__(self, handle,configure):

#     self.serialnum = sn.strip()
     self.handle = handle
     self.ch = int(configure[0])-1
     self.type = int(configure[1])
     self.name = configure[2]
     self.enabled = int(configure[3])
     self.valve = Constants.Valves[self.ch] #Labjack address name
     self.PT100 = Constants.PT100s[self.ch] #Labjack address name
     self.LED   = Constants.LEDs[self.ch]   #Labjack address name
     if self.type == 0: self.chtype="Manifold"
     if self.type == 1: self.chtype="Vent"
     if self.type == 2: self.chtype="Detector"
     self.timeATopen = 0
     self.timeATclose = 0
     self.vOpen = -1 # status unkown
     self.time = 0

   # print information
   def info(self):
     print("\nCh = %i, Type = %s, Enabled = %i, Valve = %s, PT100 = %s, LED= %s" % \
               (self.name,self.serialnum,self.ch,self.chtype,self.enabled,self.valve,self.PT100,self.LED))

   # is channel enabled
   def is_enabled(self):
     return self.enabled

   # get Name
   def get_name(self):
     return self.name

   # get Channel
   def get_ch(self):
     return self.ch

   # get Valve
   def get_valve(self):
     return self.ch+1

#   # get Serial Number
#   def get_serialnum(self):
#     return self.serialnum

   # Channel Type
   def get_type(self):
     return self.chtype

   # Get time stamp - in seconds
   def get_tstamp(self):
     self.time = time.time()
     return self.time

   # read PT100 and return (temp,volt)???
   def read_PT100(self):
     try:
       voltage = ljm.eReadName(self.handle, self.PT100) 
     except ljm.LJMError as e:
       print e
       return -999
     else:
       return voltage
   
   # read state of LED
   def LED_State(self):
     status = "Unknown"
     state = -1
     try:
       state = ljm.eReadName(self.handle, self.LED)
     except ljm.LJMError as e:
       print e
       return status
     else:
       return state

   # open valve
   def open_valve(self):
     status = "Unknown"
     self.vOpen = -1
     try:
       if self.valve.startswith("DAC"):
         voltage=3.75
         ljm.eWriteName(self.handle, self.valve,voltage)
       else:
         OPEN=1
         ljm.eWriteName(self.handle, self.valve,OPEN)
     except ljm.LJMError as e:
       print e
       return status
     else: 
       self.timeATopen = time.time()
       status = "OPEN"
       self.vOpen = 1
       return status

   # close valve
   def close_valve(self):
     status = "Unknown"
     self.vOpen = -1
     try:
       if self.valve.startswith("DAC"):
         voltage=0.0
         ljm.eWriteName(self.handle, self.valve,voltage)
       else:
         CLOSE=0
         ljm.eWriteName(self.handle, self.valve,CLOSE)
     except ljm.LJMError as e:
       print e
       return status
     else: 
       self.timeATclose = time.time()
       status = "Closed"
       self.vOpen = 0
       return status

   # is valve open
   def isVOpen(self):
     return self.vOpen

   # time valve was opened
   def time_open(self):
     return self.timeATclose - self.timeATopen

