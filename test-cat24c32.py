#!/usr/bin/python3

import argparse
from cat24c32 import CAT24C32
from random import randint
import signal
import time

parser = argparse.ArgumentParser(description='cat24c32 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=1)
args = parser.parse_args()

eeprom = CAT24C32()

outfile = None

if args.output:
    outfile = open(args.output, "w")

def cleanup(_signo, _stack):
    if outfile:
        outfile.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while True:
    address = randint(0, 0xffe) # the last byte is reserved as a serial ID, so we don't want to touch it
    writedata = randint(0, 0xff)
    try:
        eeprom.write(address, [writedata])
        readdata = eeprom.read(address)[0]
        verified = writedata == readdata

        output = f"{time.time()} 1 {address} {writedata} {verified}"
    except Exception as e:
        output = f"{time.time()} 0 {e}"
    print(output)
    if outfile:
        outfile.write(output)
        outfile.write('\n')

    if args.frequency:
        time.sleep(1.0/args.frequency)
