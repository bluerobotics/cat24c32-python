#!/usr/bin/python3

import argparse
from cat24c32 import CAT24C32
from random import randint
from pathlib import Path
import llog
import time

device = "cat24c32"
defaultMeta = Path(__file__).resolve().parent / f"{device}.meta"

parser = argparse.ArgumentParser(description=f'{device} test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=1)
args = parser.parse_args()


with llog.LLogWriter(args.meta, args.output) as log:
    eeprom = CAT24C32()

    while True:
        address = randint(0, 0xffe) # the last byte is reserved as a serial ID, so we don't want to touch it
        writedata = randint(0, 0xff)
        try:
            eeprom.write(address, [writedata])
            readdata = eeprom.read(address)[0]
            verified = writedata == readdata

            log.log(llog.LLOG_DATA, f"{address} {writedata} {verified}")
        except Exception as e:
            log.log(llog.LLOG_ERROR, e)

        if args.frequency:
            time.sleep(1.0/args.frequency)
