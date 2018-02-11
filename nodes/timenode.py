class TimeNode:
    def __init__(self, sendTime):
        self.dissemination_count = 1
        self.queue = [(sendTime, None)]
        self.avg = 0

    def setSendingTime(self, sendTime):
        self.queue.append((sendTime, None))

    def computeAvg(self, receiveTime):
        sendTime = self.queue.pop(0)[0]
        deltaT = receiveTime - sendTime
        self.avg = (self.dissemination_count * self.avg + deltaT) / (self.dissemination_count + 1)
        self.dissemination_count += 1

    def getAvg(self):
       return self.avg
