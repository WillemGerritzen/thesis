import os

import matplotlib.pyplot as plt
import pandas as pd


def graph_average_mse(dir__: str) -> None:
    columns = ['Iteration', 'Average MSE']
    algo = dir__.split('/')[-1].split('_')[-1]
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
    ax.set_ylabel(columns[1])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
    ax.set_title(f"{pretty_algo}")

    for file in os.listdir(dir__):
        df = pd.read_csv(dir__ + '/' + file, usecols=columns)
        ax.plot(df[columns[0]], df[columns[1]], label=file.removesuffix('.csv').capitalize().replace('_', ' '))
        ax.legend(prop={'size': 8})

    plt.plot()
    plt.savefig(f"results/fig/{algo}.png", bbox_inches='tight')
    plt.show()


def average_runs(algo: str) -> None:
    logs_dir = f'results/logs/'
    average_dir = logs_dir + f'average_{algo}/'

    if not os.path.exists(average_dir):
        os.mkdir(average_dir)
    else:
        for file in os.listdir(average_dir):
            os.remove(average_dir + file)

    for dir_ in os.listdir(logs_dir):
        if dir_.split('_')[0] == 'average':
            continue

        for csv in os.listdir(logs_dir + dir_):
            name = csv.lower().removeprefix("results_")

            if 'johann' in name:
                name = name.replace('johann_sebastian_', '')

            if not os.path.exists(average_dir + name):
                df = pd.read_csv(logs_dir + dir_ + '/' + csv, usecols=['Iteration', 'Average MSE'])
                df.to_csv(average_dir + name, index=False)

            else:
                df = pd.read_csv(average_dir + name)
                df['Average MSE'] += pd.read_csv(logs_dir + dir_ + '/' + csv)['Average MSE']
                df.to_csv(average_dir + name, index=False)

    for csv in os.listdir(average_dir):
        df = pd.read_csv(average_dir + csv)
        df['Average MSE'] = df['Average MSE'].div(5)
        df.to_csv(average_dir + csv, index=False)


if __name__ == '__main__':
    for algo in ['hc', 'sa', 'ppa']:
        average_runs(algo)
        graph_average_mse(f'results/logs/average_{algo}')

