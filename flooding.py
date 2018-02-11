import sys
import os

from nodes.node import Node
from nodes.timenode import TimeNode

send = 0
recv = 0
powerDictionary = {}
timeDictionary = {}

def simpleProcess(line):
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

def powerTraceLineProcess(line):

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
          powerDictionary[id] = Node(id, Tx, Rx, CPU, LPM)
       else:
          powerDictionary[id].addPowerStatistic(Tx, Rx, CPU, LPM)
       powerDictionary[id].powerTick(time, Node.computePowerUsage(Tx, Rx, CPU, LPM))

def processline(f, line):
    f(line)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--power", help="Run for powertrace log.")
    parser.add_argument("-np", "--no-powertrace", help="Run for log without powertrace.")
    args = parser.parse_args()

    if args.power is not None:
       filepath = args.power
       handle = powerTraceLineProcess
    else:
       filepath = args.no_powertrace
       handle = simpleProcess
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            processline(handle, line)
            line = fp.readline()
    print("First 5 minutes have been discarded.")
    for node in powerDictionary:
        print("Node " + str(node) + " has average power " + str(powerDictionary[node].getAvgPower()) + " mW")

    # plot power node 1
    # powerDictionary[1].plotPower()

if __name__ == "__main__":
   main()
