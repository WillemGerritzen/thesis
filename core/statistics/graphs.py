import os

import matplotlib.pyplot as plt
import pandas as pd


def graph_average_mse(dir__: str) -> None:
    vertices = dir__.split('/')[2]

    if not os.path.exists(f'results/fig/{vertices}'):
        os.makedirs(f'results/fig/{vertices}', exist_ok=True)

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
    if algo != 'sa':
        ax.set_yscale('log')
    ax.set_xlabel(columns[0] + 's')
    ax.set_ylabel(columns[1])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
    ax.set_title(f"{pretty_algo} - {vertices} Vertices")

    for file in os.listdir(dir__):
        df = pd.read_csv(dir__ + '/' + file, usecols=columns)
        ax.plot(df[columns[0]], df[columns[1]], label=file.removesuffix('.csv').capitalize().replace('_', ' '))
        ax.legend(prop={'size': 8})

    plt.plot()
    plt.savefig(f"results/fig/{vertices}/{algo}.png", bbox_inches='tight')
    plt.show()


def average_runs(algo: str) -> None:
    for vertices in [20, 100, 300, 500, 700, 1000]:
        logs_dir = f'results/log/{vertices}/'
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
                if dir_.split('_')[-1] != algo:
                    continue

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
        for vertices in [20, 100, 300, 500, 700, 1000]:
            graph_average_mse(f'results/log/{vertices}/average_{algo}')

