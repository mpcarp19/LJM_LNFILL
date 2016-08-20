from LNChannel import LNChannel

configfile = "T7-47001026.config"

file = configfile
config = open(file,"r")
content = config.readlines()
configure = 0  
numlines = 0
Detectors = []
# parse content
numdet=0
for line in content:
   if line.startswith("#Serial"):
     serialnum = line.split("=")[1].strip()
     print serialnum
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
       #print results
       if int(results[1]) == 0:
         Manifold=LNChannel(serialnum,results)
         Manifold.info()
         isOpen = Manifold.T7Status()
         if isOpen:
           print "PT100 voltage ", Manifold.read_PT100()
           print "LED State ", Manifold.LED_State()
           print "Valve is ", Manifold.close_valve()
         else:
           print "T7 with serial #%s is not reachable" % serialnum
       elif int(results[1]) == 1:
	 Vent=LNChannel(serialnum,results)
         Vent.info()
         isOpen = Vent.T7Status()
         if isOpen:
           print "PT100 voltage ", Vent.read_PT100()
           print "LED State ", Vent.LED_State()
           print "Valve is ", Vent.close_valve()
         else:
           print "T7 with serial #",serialnum," is not reachable"
       elif int(results[1]) == 2:
 	 Detectors.append(LNChannel(serialnum,results))
         Detectors[numdet].info()
         isOpen = Detectors[numdet].T7Status()
         if isOpen:
           print "PT100 voltage ", Detectors[numdet].read_PT100()
           print "LED State ", Detectors[numdet].LED_State()
           print "Valve is ", Detectors[numdet].close_valve()
         else:
           print "T7 with serial #",serialnum," is not reachable"
         numdet=numdet+1


	


