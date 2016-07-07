import logging
import statsd
import argparse
import socket
import time
import sys
import os

def main():
    last_bandwidths = get_bandwidth()

    if last_bandwidths == None:
        logger.error("Can not find interface " + interface)
        exit(1)

    while True:
        time.sleep(1)
        current_bandwidths = get_bandwidth()
        rx = round(current_bandwidths[0] - last_bandwidths[0], 2)
        tx = round(current_bandwidths[1] - last_bandwidths[1], 2)
        logger.info(interface + ": RX: {rx}MBit/s TX: {tx}MBit/s".format(rx=rx, tx=tx))
        statsd.gauge("network." + hostname + "." + interface + ".rx", rx)
        statsd.gauge("network." + hostname + "." + interface + ".tx", tx)
        last_bandwidths = get_bandwidth()

def get_bandwidth():
    f = open('/proc/net/dev', 'r')
    all = f.readlines()
    f.close()

    for dev in all:
        dev = dev.strip().split()
        if dev[0] == interface + ':':
            return (int(dev[1])/1024/1024), (int(dev[9])/1024/1024)

    return None


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s - %(name)s -> %(message)s",
        level=logging.DEBUG)

    logger = logging.getLogger("traphite")
    hostname = socket.gethostname().split('.')[0]
    logger.info("Starting up Traphite on " + hostname)

    parser = argparse.ArgumentParser(description='Traphite - Network bandwidth logging for Graphite')
    parser.add_argument('--host', help='StatsD Hostname', required=True)
    parser.add_argument('--port', help='StatsD Port', default=8125)
    parser.add_argument('--interface', help='Network interface for monitoring', default='eth0')
    args = parser.parse_args()

    interface = args.interface
    statsd = statsd.StatsClient(args.host, args.port)

    if not sys.platform == "linux" and not sys.platform == "linux2":
        logger.error("Plattform is not Linux")
        exit(1)

    if not os.path.isfile("/proc/net/dev"):
        logger.error("/proc/net/dev not found")
        exit(1)

    main()