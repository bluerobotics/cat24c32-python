#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd

def generate_figures(log):
    footer = f'ms5837 test report'

    f, spec = log.figure(height_ratios=[1,1], suptitle=f'ms5837 data', footer=footer)

    plt.subplot(spec[1,:])

    # todo check if log.error exists
    try:
        log.error.ttable(rl=True)
    except:
        pass

    plt.subplot(spec[1,:])
    counts = log.data.address.value_counts()

    map = pd.DataFrame(dict(c=counts, x=counts.index.values & 0b111111, y=counts.index.values >> 6))
    plt.scatter(map.x, map.y, s=20*map.c/map.c.max())


def main():
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages
    from pathlib import Path

    parser = LLogReader.create_default_parser(__file__, 'cat24c32')
    args = parser.parse_args()

    log = LLogReader(args.input, args.meta)

    generate_figures(log)

    if args.output:
        if Path(args.output).exists():
            print(f'WARN {args.output} exists! skipping ..')
        else:
            with PdfPages(args.output) as pdf:
                [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
