from labjack import ljm

# Open first found LabJack
#handle = ljm.openS("ANY", "ANY", "ANY")

# open a specific T7 via ethernet - we know the serial number
handle = ljm.open(ljm.constants.dtT7, ljm.constants.ctETHERNET, "470010276")

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# Call eReadName to read the serial number from the LabJack.
name = "SERIAL_NUMBER"
result = ljm.eReadName(handle, name)

print("\neReadName result: ")
print("    %s = %i" % (name, result))

# Read timer (seconds) - can be used to time events.
name = "RTC_TIME_S"
result = ljm.eReadName(handle,name)
print("\neReadName result: ")
print("    %s = %i" % (name, result))

# Setup and call eReadName to read from a AIN on the LabJack.
numPT100s = 13
PT100s = ["AIN0", "AIN1", "AIN2", "AIN3", "AIN4", "AIN5", "AIN6", "AIN7", "AIN8", "AIN9", "AIN10", "AIN11", "AIN12"]
results = ljm.eReadNames(handle, numPT100s, PT100s)

i=0
for PT100 in PT100s:
  print("%s : %f V" % (PT100, results[i]))
  i = i+1

# Digital Inputs for LEDs
numLEDs = 12
LEDs = ["CIO0", "CIO1" ,"CIO2", "CIO3", "EIO0", "EIO1" ,"EIO2", "EIO3", "EIO4", "EIO5" ,"EIO6", "EIO7"]
results = ljm.eReadNames(handle, numLEDs, LEDs)
i=0
for LED in LEDs:
  print("%s : %i State" % (LED, results[i]))
  i = i+1


# write to force direction to output
numValves = 11
Valves = ["FIO0", "FIO1" ,"FIO2", "FIO3", "FIO4", "FIO5" ,"FIO6", "FIO7", "MIO0", "MIO1" ,"MIO2"]
States = [0,1,0,1,0,1,0,1,0,1,0]
ljm.eWriteNames(handle, numValves, Valves, States)
i=0
print("here")
for Valve in Valves:
  print("%s : %i State" % (Valve, States[i]))
  i = i+1

print("all done")
ljm.close(handle)

