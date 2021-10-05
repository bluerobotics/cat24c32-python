#!/usr/bin/python3

import argparse
from cat24c32 import CAT24C32
from llog import LLogWriter
from random import randint
import time

parser = LLogWriter.create_default_parser(__file__, 'cat24c32')
args = parser.parse_args()

with LLogWriter(args.meta, args.output, console=args.console) as log:
    eeprom = CAT24C32()

    def data_getter():
        address = randint(0, 0xffe) # the last byte is reserved as a serial ID, so we don't want to touch it
        writedata = randint(0, 0xff)
        eeprom.write(address, [writedata])
        readdata = eeprom.read(address)[0]
        verified = writedata == readdata
        return f'{address} {writedata} {verified}'

    log.log_data_loop(data_getter, parser_args=args)
