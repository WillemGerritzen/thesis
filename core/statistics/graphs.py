import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

ANALYSIS_DIR = 'results/analysis'
LOG_DIR = 'results/log'


def graph_average_mse(dir__: str) -> None:
    vertices = dir__.split('/')[2]

    if not os.path.exists(f'{ANALYSIS_DIR}/fig/{vertices}'):
        os.makedirs(f'{ANALYSIS_DIR}/fig/{vertices}', exist_ok=True)

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
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    legends = format_legends([file.removesuffix('.csv') for file in os.listdir(dir__)])
    if algo == 'hc':
        bbox_to_anchor = (0.95, 0.89)
    elif algo == 'ppa':
        bbox_to_anchor = (0.95, 0.84)
    else:
        bbox_to_anchor = (0.95, 0.95)

    fig.legend(legends, frameon=False, fontsize=8, loc=1, bbox_to_anchor=bbox_to_anchor)

    plt.plot()
    plt.savefig(f"{ANALYSIS_DIR}/fig/{vertices}/average_mse_{algo}.eps", bbox_inches='tight', format='eps')
    # plt.show()


def graph_best_mse() -> None:
    csvs = [dir_ for dir_ in os.listdir(ANALYSIS_DIR) if dir_.endswith('.csv')]
    count_csvs = len(csvs)

    plt.style.use('default')
    fig, axs = plt.subplots(ncols=count_csvs, figsize=(9, 3), tight_layout=True)
    legends = []

    for count, csv in enumerate(csvs):
        df = pd.read_csv(f'{ANALYSIS_DIR}/{csv}', index_col=0)

        algo = csv.removeprefix('best_mse_').removesuffix('.csv')

        if algo == 'sa':
            pretty_algo = 'Simulated Annealing'
            y_lower_lim = 0
        elif algo == 'hc':
            pretty_algo = 'Hillclimber'
            y_lower_lim = 10
        else:
            pretty_algo = 'Plant Propagation'
            y_lower_lim = 100

        if csvs.index(csv) == count_csvs - 1:
            legends = df.columns
        if algo != 'sa':
            axs[count].set_yscale('log')
        axs[count].set_title(f"{pretty_algo}")
        axs[count].plot(df, marker='o', markersize=3)
        axs[count].spines['top'].set_visible(False)
        axs[count].spines['right'].set_visible(False)
        axs[count].set_ylim(y_lower_lim, None)

    fig.supylabel('Best MSE', x=0.01, y=0.22)
    fig.supxlabel('Vertices', y=0.03, x=0.084)
    fig.legend(format_legends(legends), loc='lower right', ncol=len(legends), frameon=False, columnspacing=0.5)

    plt.plot()
    plt.savefig(f"{ANALYSIS_DIR}/fig/best_mse.eps", bbox_inches='tight', format='eps')
    plt.show()


def average_runs_mse(algo: str) -> None:
    for vertices in [20, 100, 300, 500, 700, 1000]:
        logs_dir = f'{LOG_DIR}/{vertices}/'
        average_dir = f'{ANALYSIS_DIR}/{vertices}/average_mse_{algo}/'

        if not os.path.exists(average_dir):
            os.makedirs(average_dir, exist_ok=True)
        else:
            for file in os.listdir(average_dir):
                os.remove(average_dir + file)

        for dir_ in os.listdir(logs_dir):
            if dir_.split('_')[0] == 'average' or dir_.split('_')[0] == 'best':
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


def find_best_mse() -> None:
    dict_ = {}

    for vertices in os.listdir(LOG_DIR):
        for dir_ in os.listdir(f'{LOG_DIR}/{vertices}'):
            algo = dir_.split('_')[-1]

            if algo not in dict_:
                dict_[algo] = {}

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            for csv in os.listdir(f'{LOG_DIR}/{vertices}/{dir_}'):
                name = csv.removeprefix("results_").removesuffix(".csv")
                mse_col = 'Average MSE' if algo != 'ppa' else 'Best MSE'

                if name not in dict_[algo][vertices]:
                    dict_[algo][vertices][name] = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1]

                else:
                    current_value = dict_[algo][vertices][name]
                    new_value = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1]
                    if new_value < current_value:
                        dict_[algo][vertices][name] = new_value

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        df.to_csv(f'{ANALYSIS_DIR}/best_mse_{algo}.csv', index_label='vertices')


def format_legends(legends: List[str]) -> List[str]:
    pretty_legends = []
    for legend in legends:
        if legend == 'convergence':
            legend = 'Pollock'

        elif legend == 'the_kiss':
            legend = 'Klimt'

        elif legend == 'the_persistence_of_memory':
            legend = 'Dali'

        else:
            legend = legend.replace('_', ' ')

            if ' ' in legend:
                legend = legend.split(' ')[0].capitalize() + ' ' + legend.split(' ')[1].capitalize()
            else:
                legend = legend.capitalize()

        pretty_legends.append(legend)

    return pretty_legends


if __name__ == '__main__':
    # find_best_mse()
    graph_best_mse()

    # for algo in ['sa', 'hc', 'ppa']:
    #     # average_runs_mse(algo)
    #     for vertices in [20, 100, 300, 500, 700, 1000]:
    #         graph_average_mse(f'{ANALYSIS_DIR}/{vertices}/average_mse_{algo}')

