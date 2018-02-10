class Node:
    def __init__(self, Tx, Rx, CPU, LPM):
        self.power_count = 1
        self.avg_power = self._computePowerUsage(Tx, Rx, CPU, LPM)

    def addPowerStatistic(self, Tx, Rx, CPU, LPM):
        newP = self._computePowerUsage(Tx, Rx, CPU, LPM)
        self.avg_power = (self.power_count * self.avg_power + newP) / (self.power_count + 1)
        self.power_count += 1

    def _computePowerUsage(self, Tx, Rx, CPU, LPM):
        return ((19.5 * Tx + 21.8 * Rx + 1.8 * CPU + 0.0545 * LPM) * 3) / 327680

    def getAvgPower(self):
        return self.avg_power
