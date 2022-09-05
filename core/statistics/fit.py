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
        'hc_ffa': {
            'p0': (800000, -2000, 0.6, 13000),
            'file': '../../results/analysis/100/average_mse_hc_ffa/mondriaan_plot.csv',
            'columns': ['Iteration', 'MSE'],
            'color': 'tab:blue',
            'pickle': '../../results/analysis/mondriaan_ffa.pickle'
        },
        'hc_no_ffa': {
            'p0': (800000, -2000, 0.55, 10000),
            'file': '../../results/analysis/100/average_mse_hc/mondriaan.csv',
            'columns': ['Iteration', 'Average MSE'],
            'color': 'tab:orange',
            'pickle': '../../results/analysis/mondriaan.pickle'
        },
        'ppa_ffa': {
            'p0': (800000, -2000, 0.6, 13000),
            'file': '../../results/analysis/20/average_mse_ppa_ffa/convergence_plot.csv',
            'columns': ['Iteration', 'MSE'],
            'color': 'tab:blue',
            'pickle': '../../results/analysis/convergence_ffa.pickle'
        },
        'ppa_no_ffa': {
            'p0': (800000, -2000, 0.55, 10000),
            'file': '../../results/analysis/20/average_mse_ppa/convergence.csv',
            'columns': ['Iteration', 'Average MSE'],
            'color': 'tab:orange',
            'pickle': '../../results/analysis/convergence.pickle'
        },
        'sa_ffa': {
            'p0': (800000, -2000, 0.6, 13000),
            'file': '../../results/analysis/1000/average_mse_sa_ffa/mona_lisa_plot.csv',
            'columns': ['Iteration', 'MSE'],
            'color': 'tab:blue',
            'pickle': '../../results/analysis/mona_lisa_ffa.pickle'
        },
        'sa_no_ffa': {
            'p0': (800000, -2000, 0.55, 10000),
            'file': '../../results/analysis/1000/average_mse_sa/mona_lisa.csv',
            'columns': ['Iteration', 'Average MSE'],
            'color': 'tab:orange',
            'pickle': '../../results/analysis/mona_lisa.pickle'
        }
    }

    fig, axs = plt.subplots(3, 1, sharex='all', figsize=(5, 4.5), tight_layout=True)

    full_legend = []
    algo_check = ['hc', 'ppa', 'sa']
    y_label = ['1.', '2.', '3.']
    for algo, data in meta_data.items():
        plt_idx = algo_check.index(algo.split('_')[0])
        columns = data['columns']
        df = pd.read_csv(data['file'], usecols=columns)
        try:
            constants = pickle.load(open(data['pickle'], 'rb'))
        except FileNotFoundError:
            constants = curve_fit(mse_eval, df[columns[0]], df[columns[1]], p0=data['p0'], maxfev=1000000)
            pickle.dump(constants, open(data['pickle'], 'wb'))
        a, b, c, d = constants[0]
        axs[plt_idx].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
        axs[plt_idx].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
        axs[plt_idx].spines['right'].set_visible(False)
        axs[plt_idx].spines['top'].set_visible(False)
        axs[plt_idx].plot(df[columns[0]], df[columns[1]], color=data['color'], alpha=0.7)
        axs[plt_idx].plot(np.arange(0, 5000000, 1000), mse_eval(np.arange(0, 5000000, 1000), a, b, c, d), '--', color=data['color'])
        axs[plt_idx].set_ylabel(y_label[plt_idx], rotation=0, labelpad=10)
        fig.supylabel('MSE')
        fig.supxlabel('Function evaluations')
        fig.legend(['FFA', 'FFA - projection', 'No FFA', 'No FFA - projection'])
        axs[plt_idx].axvline(x=999999, color='grey', alpha=0.7)
    # plt.savefig('../../results/analysis/mondriaan_ffa_no_ffa.png')
    plt.show()


def test():
    p = pickle.load(open('../../results/analysis/mondriaan_ffa.pickle', 'rb'))
    print(p)


if __name__ == '__main__':
    fit_curve()
    # test()
