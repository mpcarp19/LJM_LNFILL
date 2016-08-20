
import Constants.py

class Manifold:

   ''' Creat a Manifold object - associates only a vavle to it'''

   def __init__(self, configure):

     self.ch = (int)configure[0];
     self.type = (int)configure[1];
     self.name = configure[2];
     self.enabled = configure[3];
     self.valve = Valves[self.ch]
     self.PT100 = "null"
     self.LED   = "null"
