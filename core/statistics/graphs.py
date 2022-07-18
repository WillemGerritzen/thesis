import os

import matplotlib.pyplot as plt
import pandas as pd


def graph_average_mse(dir__: str) -> None:
    columns = ['Iteration', 'Average MSE']
    algo, run = dir__.split('/')[-1][2:], dir__.split('/')[-1][0]
    pretty_algo = ""

    if algo == 'sa':
        pretty_algo = 'Simulated Annealing'
    elif algo == 'hc':
        pretty_algo = 'Hill Climber'
    elif algo == 'ppa':
        pretty_algo = 'Plant Propagation Algorithm'

    plt.style.use('default')

    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_xlabel(columns[0] + 's')
    ax.set_ylabel('MSE')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
    ax.set_title(f"Run {run} - {pretty_algo}")

    for file in os.listdir(dir__):
        df = pd.read_csv(dir__ + '/' + file, usecols=columns)
        ax.plot(df[columns[0]], df[columns[1]], label=file[8:-4].replace('_', ' '))
        ax.legend(prop={'size': 8})

    plt.plot()
    plt.savefig(f"results/fig/{run}_{algo}.png", bbox_inches='tight')
    # plt.show()


if __name__ == '__main__':
    for dir_ in os.listdir('results/logs/'):
        graph_average_mse(f'results/logs/{dir_}')
