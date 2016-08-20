from LNType import Manifold, Detector, Vent

class LNFillController:

   '''LNFillSystem will allow one to control the LNFill Module 
      designed and built by P. Wilt using the T7 labjack'''

   def __init__(self, configfile):

     self.file = configfile
     config = open(self.file,"r")
     content = config.readlines()
     configure = 0  
     numlines = 0 
     numdet = 0
     # parse content
     for line in content
       if .text.startswith("#Serial"):
         self.serialnum = line.split("=")[1]
     elif line.startswith("#Config"):
       configure=1
     elif line.startswith("#"):
        numline = 0
     elif configure==1:
       results = line.split(",")
       if len(results) == 4:
         i = 0
         for result in results:  
           results[i] = result.strip()
           i=i+1
         print results
         if int(results[1]) == 0:
           Manifold=Manifold(self.serialnum,results)
           Manifold.info()
         elif int(results[1]) == 1:
	   Vent=Vent(self.serialnum,results)
           Vent.info()
         elif int(results[1]) == 2:
 	   Detectors.append(Detector(self.serialnum,results))
           Detectors[numdet].info()
           numdet=numdet+1

