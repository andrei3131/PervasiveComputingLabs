Goals of the tutorial: dissemination time and power usage

Sending rate = 6 packets/min
Note, when modifying the send interval in udp_client.c,
it initially sends a packet every second.

Note: when calculating dissemination time for mote i, you can use:
number of packets send to server from node i - number of packets received
by the server from node i

Note: there is no send in the logs because the debug flag was switched off.
Note: we can use the log from last time to get the times. think of multiple cases of packet send-receive order for calculating the dissemination time
