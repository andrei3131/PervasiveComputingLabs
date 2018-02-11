import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

class Node:
    def __init__(self, id, Tx, Rx, CPU, LPM):
        self.id = id
        self.power_count = 1
        self.avg_power = Node.computePowerUsage(Tx, Rx, CPU, LPM)
        self.time = []
        self.power = []

    def addPowerStatistic(self, Tx, Rx, CPU, LPM):
        newP = Node.computePowerUsage(Tx, Rx, CPU, LPM)
        self.avg_power = (self.power_count * self.avg_power + newP) / (self.power_count + 1)
        self.power_count += 1

    # Static method
    def computePowerUsage(Tx, Rx, CPU, LPM):
        return ((19.5 * Tx + 21.8 * Rx + 1.8 * CPU + 0.0545 * LPM) * 3) / 327680

    def getAvgPower(self):
        return self.avg_power

    def powerTick(self, currentTime, power):
        t = datetime.strptime(currentTime, '%M:%S.%f')
        self.time.append(t)
        self.power.append(power)

    def plotPower(self):
        fig = plt.figure()
        plt.plot(self.time, self.power)
        plt.axhline(y=self.avg_power, color='r', linestyle='-', label='Average power consumption')

        fig.suptitle("Power Consumption Node " + str(self.id), fontsize=12)
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Power usage', fontsize=16)
        plt.legend()

        formatter = DateFormatter('%M:%S')
        plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
        plt.show()
