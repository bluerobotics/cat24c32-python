#!/usr/bin/python3

import argparse
from cat24c32 import CAT24C32
from random import randint
import time

parser = argparse.ArgumentParser(description='cat24c32 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=1)
args = parser.parse_args()

if args.frequency < 1:
    args.frequency = 1

eeprom = CAT24C32()

if args.output:
    outfile = open(args.output, "w")

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
    if args.output:
        outfile.write(output)
        outfile.write('\n')

    time.sleep(1.0/args.frequency)

# this is never reached, but works anyway in practice
# todo handle KeyboardInterrupt for ctrl+c
if args.output:
    outfile.close()
