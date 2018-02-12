import sys
import os

from nodes.node import Node
from nodes.timenode import TimeNode
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

powerDictionary = {}
disseminationMap = {}
disseminationTimeMap = {}

class NodeDisseminations:
    def __init__(self, dissemination_id, currentTime):
        self.disseminations_for_node = {}
        self.disseminations_for_node[dissemination_id] = DeltaTime(currentTime)

    def updateLastReceive(self, dissemination_id, currentTime):
        self.disseminations_for_node[dissemination_id].updateLastReceiveAt(currentTime)

    def computeAvgDisseminationTimeForNode(self):
        s = 0
        for dissemination in self.disseminations_for_node:
            deltaTime = self.disseminations_for_node[dissemination]
            if deltaTime.isValid():
                s += deltaTime.getTimeDifference()
        return s / len(self.disseminations_for_node)

class DeltaTime:
    def __init__(self, sentAt):
        self.sentAt = sentAt
        self.lastReceiveAt = None

    def updateLastReceiveAt(self, time):
        self.lastReceiveAt = time

    def isValid(self):
        return self.lastReceiveAt is not None

    def getTimeDifference(self):
        return self.lastReceiveAt - self.sentAt

def plotE2E():
    dissemination_ids = [d for d in disseminationMap]
    e2e_gains = [disseminationMap[d] / 30 for d in disseminationMap]
    fig = plt.figure()
    plt.plot(dissemination_ids, e2e_gains, marker='o')
    s = 0
    for dissemination in disseminationMap:
        e2e = disseminationMap[dissemination] / 30
        s += e2e
    plt.axhline(y=s / len(disseminationMap), color='r', linestyle='-', label='Average E2E gain rate ' + '%.3f'%(100 * s / len(disseminationMap)) + "%")

    fig.suptitle("E2E Gain Rate", fontsize=12)
    plt.xlabel('Dissemination ID', fontsize=18)
    plt.ylabel('Percentage', fontsize=16)
    plt.legend()

    plt.gcf().axes[0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    plt.show()

def plotDisseminationTime():
    node_ids = [n for n in disseminationTimeMap]
    avgs_per_node = [disseminationTimeMap[n].computeAvgDisseminationTimeForNode() for n in disseminationTimeMap]
    fig = plt.figure()
    plt.plot(node_ids, avgs_per_node, marker='x', markersize=3)

    s = 0
    for originating_node in disseminationTimeMap:
        nodeDisseminations = disseminationTimeMap[originating_node]
        s += nodeDisseminations.computeAvgDisseminationTimeForNode()

    plt.axhline(y=s / len(disseminationTimeMap), color='r', linestyle='-', label='Average dissemination time ' + '%.3f'%(s / 30) + "ms")

    plt.gca().set_ylim([0, 200])
    fig.suptitle("Dissemination Time Graph Per Node", fontsize=12)
    plt.xlabel('Node ID', fontsize=18)
    plt.ylabel('Average node dissemination time', fontsize=16)
    plt.legend()

    plt.show()


def simpleProcess(line):
    #discard first five minutes
    if int(line.split(':', 1)[0]) < 5:
        return None

    metadata = line.split(" ", 1)[0].split("\t")
    id = int(metadata[1].split(":")[1])

    time = metadata[0].split(":")
    minutes = int(time[0])
    seconds = float(time[1])
    currentTimeMilliseconds = (minutes * 60 + seconds) * 1000

    line = line.rstrip('\n')
    potential_dissemination_id = line.split(" ")[-1]
    if("Broadcast message sent" in line and potential_dissemination_id.isdigit()):
        dissemination_id = int(potential_dissemination_id)
        record = set()
        record.add(id)
        disseminationMap[dissemination_id] = record
        # id is the id of the originating node
        disseminationTimeMap[id] = NodeDisseminations(dissemination_id, currentTimeMilliseconds)
    if("Broadcast recv from" in line and line.split(" ")[-1].isdigit()):
        dissem_id = int(line.split(" ")[-1])
        disseminationMap[dissem_id].add(id)

        originating_node = int(line.split(" ")[-4])
        disseminationTimeMap[originating_node].updateLastReceive(dissem_id, currentTimeMilliseconds)
        # Debug the outlier: for id 195: sentAt = 00:34:54,  lastReceiveAt = 00:35:24
        # if(disseminationTimeMap[id].getTimeDifference() > 30000):
        #   import pdb; pdb.set_trace()


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

def printPowerSummary():
    for node in powerDictionary:
        print("Node " + str(node) + " has average power " + str(powerDictionary[node].getAvgPower()) + " mW")

def printE2ESummary():
    s = 0
    for dissemination in disseminationMap:
        e2e = len(disseminationMap[dissemination]) / 30
        s += e2e
        print("Dissemination " + str(dissemination) + ": " + '%.3f'%(e2e * 100) + "% nodes received an update.")
    print("Average E2E-Loss rate is " + str(s / len(disseminationMap)) + "\n")

def printDisseminationTimeSummary():
    s = 0
    for originating_node in disseminationTimeMap:
        nodeDisseminations = disseminationTimeMap[originating_node]
        s += nodeDisseminations.computeAvgDisseminationTimeForNode()
        print("Node " + str(originating_node) + " has dissemination time: " + str(nodeDisseminations.computeAvgDisseminationTimeForNode()) + "ms")
    print("Average dissemination time is " + str(s / 30) + "ms\n")


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
    print("Note: First 5 minutes have been discarded.")
    if args.power is not None:
       print("Power consumption summary:")
       printPowerSummary()
       # plot power node 1
       # powerDictionary[1].plotPower()

    if args.no_powertrace is not None:
       print("E2E loss/gain rate summary:")
       printE2ESummary()
       #plotE2E()
       print("Dissemination time summary:")
       printDisseminationTimeSummary()
       plotDisseminationTime()

if __name__ == "__main__":
   main()
