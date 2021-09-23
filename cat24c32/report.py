#!/usr/bin/python3

import matplotlib.pyplot as plt

log = None

def main():
    import argparse
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))

    defaultMeta = dir_path + '/cat24c32.meta'
    parser = argparse.ArgumentParser(description='cat24c32 test report')
    parser.add_argument('--input', action='store', type=str, required=True)
    parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
    parser.add_argument('--output', action='store', type=str)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    log = LLogReader(args.input, args.meta)

    counts = log.data.address.value_counts()

    import pandas as pd
    map = pd.DataFrame(dict(c=counts, x=counts.index.values & 0b111111, y=counts.index.values >> 6))
    plt.scatter(map.x, map.y, s=20*map.c/map.c.max())
    plt.show()
    if args.output:
        # todo check if it exists!
        with PdfPages(args.output) as pdf:
            [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
