import sys
import os

send = 0
recv = 0
powerDictionary = {}

def registerPDRdata(line):
    global send
    global recv
    if("DATA send" in line):
        send += 1
    if("DATA recv" in line):
        recv += 1

def printPDR():
    global send
    global recv
    if send != 0:
        print("PDR is " + str(recv * 100 / send))
    else:
        print("No packet was sent.")

def computePowerUsage(Tx, Rx, CPU, LPM):
    return ((19.5 * Tx + 21.8 * Rx + 1.8 * CPU + 0.0545 * LPM) * 3) / 327680

def processline(line):
    registerPDRdata(line)

    #discard first five minutes
    if int(line.split(':', 1)) < 5:
        print("First 5 minutes have been discarded.")
        return None

    #add dictionary from node id to set of powerUsage values and plot them using
    # differences of successive values



def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            processline(line)
            line = fp.readline()
    printPDR()

if __name__ == "__main__":
   main()
