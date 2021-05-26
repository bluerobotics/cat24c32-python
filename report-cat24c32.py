#!/usr/bin/python3

import argparse
from datetime import datetime
from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

WIDTH = 210
HEIGHT = 297

file_path = './tmp/'
if not os.path.exists(file_path):
    os.makedirs(file_path)

# TODO Can I put this into a function?
parser = argparse.ArgumentParser(description='cat24c32 test')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()

data = pd.read_csv(args.input, header=None, sep=' ')
data.rename(columns={0: "Timestamp", 1: "Log_Type"}, inplace=True)
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
print(data.head())

measurements = pd.DataFrame(data=data.query('Log_Type == 1'))
measurements.rename(columns={2: "Address", 3: "Data", 4: "Verified"}, inplace=True)
print(measurements.head())

errors = pd.DataFrame(data=data.query('Log_Type == 0'))
errors.rename(columns={2: 'Error Message'}, inplace=True)


def generate_table():
    # Errors
    error_list = None
    ts_list = None

    if not errors.empty:
        error_list = errors['Error Message'].tolist()
        ts_list = errors['Timestamps'].to_list()

    length = len(measurements['Verified'])
    verified_true = pd.DataFrame(data=measurements.query('Verified == True'))
    length_true = len(verified_true['Verified'])

    if length == length_true:
        eeprom_pass = True
    else:
        eeprom_pass = False

    return length, length_true, eeprom_pass, error_list, ts_list


def table_helper(pdf, epw, th, table_data, col_num):
    for row in table_data:
        for datum in row:
            # Enter data in columns
            pdf.cell(epw/col_num, 2 * th, str(datum), border=1)
        pdf.ln(2 * th)


def init_report(filename=args.output):
    length, length_true, eeprom_pass, error_list, ts_list = generate_table()

    error_data = [ts_list, error_list]
    result_data = [['Count Data Sent', 'Data Verified True', 'Test Result'], [length, length_true, eeprom_pass]]
    pdf = FPDF()
    epw = pdf.w - 2*pdf.l_margin
    pdf.add_page()

    pdf.set_font('Helvetica', '', 10.0)
    th = pdf.font_size

    if None not in result_data:
        pdf.set_font('Helvetica', '', 14.0)
        pdf.cell(WIDTH, 0.0, 'Summary of EEPROM Test', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, result_data, 3)
        pdf.ln(5)

    if None not in error_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of EEPROM Test Errors', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, error_data, len(error_list))
        pdf.ln(5)

    pdf.output(filename, 'F')


if __name__ == '__main__':
    print("Post-Processing Script")
    generate_table()
    init_report()
