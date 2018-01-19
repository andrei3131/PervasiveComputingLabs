import sys
import os

send = 0
recv = 0

def processline(line):
    global send
    global recv
    if("DATA send" in line):
        send += 1
    if("DATA recv" in line):
        recv += 1
        
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
    if send != 0:
        print("PDR is " + str(recv * 100 / send))
    else:
        print("No packet was sent.")

if __name__ == "__main__":
   main()
