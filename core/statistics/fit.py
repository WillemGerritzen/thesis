import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from core.statistics.graphs import format_number


def mse_eval(x, a, b, c, d) -> float:
    return a * np.power((x - b), -c) + d


def fit_curve() -> None:
    meta_data = {
        'ffa': {
            'p0': (800000, -2000, 0.6, 13000),
            'file': '../../results/analysis/100/average_mse_hc_ffa/mondriaan_plot.csv',
            'columns': ['Iteration', 'MSE'],
            'color': 'red',
            'pickle': '../../results/analysis/mondriaan_ffa.pickle'
        },
        'no_ffa': {
            'p0': (800000, -2000, 0.55, 10000),
            'file': '../../results/analysis/100/average_mse_hc/mondriaan.csv',
            'columns': ['Iteration', 'Average MSE'],
            'color': 'blue',
            'pickle': '../../results/analysis/mondriaan.pickle'
        }
    }

    fig, ax = plt.subplots()

    for data in meta_data.values():
        columns = data['columns']
        df = pd.read_csv(data['file'], usecols=columns)
        try:
            constants = pickle.load(open(data['pickle'], 'rb'))
        except FileNotFoundError:
            constants = curve_fit(mse_eval, df[columns[0]], df[columns[1]], p0=data['p0'], maxfev=1000000)
            pickle.dump(constants, open(data['pickle'], 'wb'))
        a, b, c, d = constants[0]
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
        ax.set_xlabel('Function Evaluations')
        ax.set_ylabel('MSE')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.suptitle('Mondriaan - HC - 100 v.')
        # plt.axvline(x=999999, color='grey')
        plt.plot(df[columns[0]], df[columns[1]], color=data['color'], alpha=0.5)
        plt.plot(np.arange(0, 10000000, 1000), mse_eval(np.arange(0, 10000000, 1000), a, b, c, d), '--', color=data['color'])
        plt.legend(['FFA', 'FFA - projection', 'No FFA', 'No FFA - projection'], )
    plt.savefig('../../results/analysis/mondriaan_ffa_no_ffa.png')
    plt.show()


def test():
    p = pickle.load(open('../../results/analysis/mondriaan_ffa.pickle', 'rb'))
    print(p)


if __name__ == '__main__':
    fit_curve()
    # test()
