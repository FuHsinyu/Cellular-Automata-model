"""
Demonstration of how matplotlib can be used to draw the results of your
parameter sweep, parsing a single .csv file provided via commandline argument.

This file is intended to provide a basis for students who want to analyze and
plot their results using Python, and should therefore be modified further with
the desired functionality.
"""

import csv
import sys

import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Usage: %s filename" % sys.argv[0])
        return

    data = None
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # First row contains names of all params. Every other row begins with the
    # values of those params (including the repetition count), and an empty
    # cell.
    num_params = len(data[0])
    legend = []
    for row in data[1:]:
        legend.append(','.join(row[:num_params]))
        plt.plot(row[num_params + 1:])
    plt.legend(legend)
    plt.show()

if __name__ == '__main__':
    main()
