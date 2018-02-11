import sys
import os

from nodes.node import Node
from nodes.timenode import TimeNode
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

powerDictionary = {}
disseminationMap = {}

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
        disseminationMap[dissemination_id] = 0
    if("Broadcast recv from" in line and line.split(" ")[-1].isdigit()):
        id = int(line.split(" ")[-1])
        disseminationMap[id] += 1


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
    s = 0
    for dissemination in disseminationMap:
        e2e = disseminationMap[dissemination] / 30
        s += e2e
        print("Dissemination " + str(dissemination) + ": " + '%.3f'%(e2e * 100) + "% nodes received an update.")
    print("Average E2E-Loss rate is " + str(1 - s / len(disseminationMap)))
    plotE2E()

if __name__ == "__main__":
   main()
