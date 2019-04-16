#!/Users/kopf/.virtualenvs/matplotlib/bin/frameworkpython
import datetime
import json
import sys

import matplotlib.pyplot as plt
import numpy as np

START_DATE = datetime.date(2014, 6, 2) # Real start date
#START_DATE = datetime.date(2014, 6, 7) # After the initial spike of signups
END_DATE = datetime.datetime.now().date()


def plot_timeseries(stats_path, cumulative=False):
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    delta = END_DATE - START_DATE
    dates = [START_DATE + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    values = []
    for date in dates:
        values.append(stats.get(date.strftime('%Y-%m-%d'), 0))
    if cumulative:
        for idx, value in enumerate(values):
            if idx > 0:
                values[idx] = values[idx] + values[idx-1]

    plt.plot(dates, values)
    plt.show()


if __name__ == '__main__':
    plot_timeseries(sys.argv[-1], cumulative=True)