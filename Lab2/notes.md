Goals of the tutorial: dissemination time and power usage

Sending rate = 6 packets/min
Note, when modifying the send interval in udp_client.c,
it initially sends a packet every second.

Note: when calculating dissemination time for mote i, you can use:
number of packets send to server from node i - number of packets received
by the server from node i

Note: there is no send in the logs because the debug flag was switched off.
Note: we can use the log from last time to get the times. think of multiple cases of packet send-receive order for calculating the dissemination time


Comparison Random topology vs line topology:

Random Topology:
First 5 minutes have been discarded.
PDR is 55.357142857142854%
Node 2 has average power 54.30105387655403 mW
Node 3 has average power 54.1855824620565 mW
Node 4 has average power 54.45646417573364 mW
Node 5 has average power 54.33133210863383 mW
Node 6 has average power 54.46677082053383 mW
Node 7 has average power 54.27660027214303 mW
Node 8 has average power 54.45472606975849 mW
Node 9 has average power 54.4655144162021 mW
Node 10 has average power 54.22858956107676 mW
Node 2 has average dissemination time 223.15833333333345 ms
Node 3 has average dissemination time 219.336134453782 ms
Node 4 has average dissemination time 0 ms
Node 5 has average dissemination time 21.225000000000836 ms
Node 6 has average dissemination time 0 ms
Node 7 has average dissemination time 35.23529411764927 ms
Node 8 has average dissemination time 0 ms
Node 9 has average dissemination time 0 ms
Node 10 has average dissemination time 134.53448275861948 ms

Line Topology:
First 5 minutes have been discarded.
PDR is 99.62476547842401%
Node 2 has average power 54.214882007707864 mW
Node 3 has average power 53.94672701227822 mW
Node 4 has average power 54.159369653018494 mW
Node 5 has average power 54.06112408467385 mW
Node 6 has average power 54.14983759037899 mW
Node 7 has average power 54.17486667737017 mW
Node 8 has average power 54.21660845665564 mW
Node 9 has average power 54.26441236468305 mW
Node 10 has average power 54.32691017253163 mW
Node 2 has average dissemination time 26.708333333336306 ms
Node 3 has average dissemination time 115.84999999999954 ms
Node 4 has average dissemination time 250.07563025209754 ms
Node 5 has average dissemination time 323.15966386554464 ms
Node 6 has average dissemination time 500.1428571428551 ms
Node 7 has average dissemination time 631.0249999999978 ms
Node 8 has average dissemination time 10763.168067226883 ms
Node 9 has average dissemination time 10853.627118644059 ms
Node 10 has average dissemination time 20993.965811965812 ms
