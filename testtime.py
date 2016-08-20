from LNChannel import LNChannel
import time

def loggit(f,logstr):	
  print logstr
  f.write(logstr + "\n")
  return

date = time.localtime(time.time())
datestr = time.strftime("%Y%m%d.%H%M",date)
logfile="FillA."+datestr+".LOG"
print logfile
f = open(logfile,"w")
logstr = "Filling Log of Side A"
loggit(f,logstr)
a=245.66666
i=int(a+1)
stra = "%.2f abc" % a
#logstr = "Number of Enabled Manifolds " + str(i)
loggit(f,"Number of Enabled Manifolds " + stra )


