import sys
import os

from nodes.node import Node
from nodes.timenode import TimeNode

send = 0
recv = 0
powerDictionary = {}
timeDictionary = {}

def registerPDRdata(line):
    global send
    global recv
    metadata = line.split(" ", 1)[0].split("\t")
    id = int(metadata[1].split(":")[1])

    time = metadata[0].split(":")
    minutes = int(time[0])
    seconds = float(time[1])
    currentTimeMilliseconds = (minutes * 60 + seconds) * 1000

    if("DATA send" in line):
        if id in timeDictionary:
           timeDictionary[id].setSendingTime(currentTimeMilliseconds)
        else:
           timeDictionary[id] = TimeNode(currentTimeMilliseconds)
        send += 1
    if("DATA recv" in line):
        senderId = int(line.split(" ")[-1])
        if senderId not in timeDictionary:
            sys.exit()
        else:
            timeDictionary[senderId].computeAvg(currentTimeMilliseconds)
        recv += 1

def printPDR():
    global send
    global recv
    if send != 0:
        print("PDR is " + str(recv * 100 / send) + "%")
    else:
        print("No packet was sent.")


def processline(line):
    registerPDRdata(line)

    #discard first five minutes
    if int(line.split(':', 1)[0]) < 5:
        return None

    # add dictionary from node id to set of powerUsage values and plot them using
    # differences of successive values or ~simply compute average~
    tokens = line.split(" ")
    if "P" in tokens and "#P" not in tokens[0]:
       nodeinfo = tokens[0].split("\t")
       time = nodeinfo[0]
       id = int(nodeinfo[1].split(":")[1])

       Tx = int(tokens[11])
       Rx = int(tokens[12])
       CPU = int(tokens[13])
       LPM = int(tokens[14])
       if id not in powerDictionary:
          powerDictionary[id] = Node(Tx, Rx, CPU, LPM)
       else:
          powerDictionary[id].addPowerStatistic(Tx, Rx, CPU, LPM)


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
    print("First 5 minutes have been discarded.")
    printPDR()
    for node in powerDictionary:
        print("Node " + str(node) + " has average power " + str(powerDictionary[node].getAvgPower()) + " mW")
    for node in timeDictionary:
        print("Node " + str(node) + " has average dissemination time " + str(timeDictionary[node].getAvg()) + " ms")


if __name__ == "__main__":
   main()
