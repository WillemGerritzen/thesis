import os
import pprint
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors

from core.statistics.graphs import format_legends, format_number

ANALYSIS_DIR = 'results/analysis'
LOG_DIR = 'results/log'


def graph_average_mse() -> None:
    vertices = [20, 100, 300, 500, 700, 1000]
    algos = ['hc', 'ppa', 'sa']
    algo_mapping = {
        'sa': {'title': 'Simulated annealing'},
        'hc': {'title': 'Hill climber'},
        'ppa': {'title': 'Plant propagation'}
    }
    figsize_ratio = (2.5, 3)
    columns = ['Iteration', 'MSE']

    title_size = 22
    axis_label_size = 14
    legend_size = 10
    size_subplots_mult = 3.2

    plt.style.use('default')
    fig = plt.figure(figsize=tuple([x * size_subplots_mult for x in figsize_ratio]), constrained_layout=True)
    subfigs = fig.subfigures(3, 1)
    fig.suptitle('Average MSE', fontsize=title_size, color='white')  # Creates space for the legends
    fig.supxlabel('Function Evaluations', size=axis_label_size, weight='bold')
    fig.supylabel('Average MSE', size=axis_label_size, weight='bold')

    for algo in algos:
        axs = subfigs[algos.index(algo)].subplots(ncols=len(vertices), sharex=True, sharey=True)
        subfigs[algos.index(algo)].supylabel(algo_mapping[algo]['title'])

        for count_v, vertice in enumerate(vertices):
            average_dir = f'{ANALYSIS_DIR}/{vertice}/average_mse_{algo}_ffa/'

            if not os.path.exists(f'{ANALYSIS_DIR}/fig/{vertice}'):
                os.makedirs(f'{ANALYSIS_DIR}/fig/{vertice}', exist_ok=True)

            for count_a, ax in enumerate(axs):
                if count_a == count_v:
                    # ax.set_ylim(algo_mapping[algo]['ylim'])
                    # ax.set_yscale(algo_mapping[algo]['yscale'])

                    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                    if ax.get_yscale() == 'linear':
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))

                    if algos.index(algo) == 0:
                        ax.set_title(f"{vertice} Vert.")

                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)

                    legends = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
                               'the_persistence_of_memory']

                    if count_a == 0:
                        pretty_legends = format_legends(legends)
                        fig.legend(pretty_legends, frameon=False, fontsize=legend_size, loc='center',
                                   ncol=len(pretty_legends), columnspacing=1, bbox_to_anchor=(0.5, 0.99))

                    for image in legends:
                        df = pd.read_csv(f'{average_dir}{image}_plot.csv', usecols=columns)
                        ax.plot(df[columns[0]], df[columns[1]],
                                label=image)

    plt.plot()
    plt.savefig(f"{ANALYSIS_DIR}/fig/average_mse_ffa.png", bbox_inches='tight', format='png')
    plt.show()


def average_runs_mse() -> None:
    for algo in ['sa', 'ppa', 'hc']:
        columns = ['Iteration', 'Average MSE']
        for vertices in [20, 100, 300, 500, 700, 1000]:
            logs_dir = f'{LOG_DIR}/{vertices}/'
            average_dir = f'{ANALYSIS_DIR}/{vertices}/average_mse_{algo}/'

            if not os.path.exists(average_dir):
                os.makedirs(average_dir, exist_ok=True)
            else:
                for file in os.listdir(average_dir):
                    os.remove(average_dir + file)

            for dir_ in os.listdir(logs_dir):
                if 'ffa' in dir_ or 'sa' not in dir_:
                    continue
                for csv in os.listdir(logs_dir + dir_):
                    name = csv.lower().removeprefix("results_")

                    if 'johann' in name:
                        name = name.replace('johann_sebastian_', '')

                    if not os.path.exists(average_dir + name):
                        df = pd.read_csv(logs_dir + dir_ + '/' + csv, usecols=columns)
                        df.to_csv(average_dir + name, index=False)

                    else:
                        df = pd.read_csv(average_dir + name)
                        df[columns[1]] += pd.read_csv(logs_dir + dir_ + '/' + csv)[columns[1]]
                        df.to_csv(average_dir + name, index=False)

            for csv in os.listdir(average_dir):
                df = pd.read_csv(average_dir + csv)
                df[columns[1]] = df[columns[1]].div(5)
                df.to_csv(average_dir + csv, index=False)


def find_best_run() -> Dict[str, Dict[str, Tuple[str, float]]]:
    dict_ = {}

    for vertices in os.listdir(LOG_DIR):
        for dir_ in os.listdir(f'{LOG_DIR}/{vertices}'):
            if not dir_.endswith('ffa'):
                continue

            algo = dir_.split('_')[1]

            if algo not in dict_:
                dict_[algo] = {}

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            run_dir = f'{LOG_DIR}/{vertices}/{dir_}'
            avg_mse = 0
            count_images = len([x for x in os.listdir(run_dir) if x.endswith('.csv')])

            for csv in sorted(os.listdir(run_dir)):
                if not csv.endswith('.csv'):
                    continue
                mse_col = 'Average MSE' if algo != 'ppa' else 'Best MSE'

                avg_mse += pd.read_csv(f'{run_dir}/{csv}', usecols=[mse_col])[mse_col].min()

            avg_mse /= count_images
            if not dict_[algo][vertices]:
                dict_[algo][vertices] = run_dir, avg_mse
            else:
                dict_[algo][vertices] = (run_dir, avg_mse) if avg_mse < dict_[algo][vertices][1] else dict_[algo][
                    vertices]

    return dict_


def plot_new_sa() -> None:
    columns = ['Iteration', 'Average MSE']
    images = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss', 'the_persistence_of_memory']
    vertices = [20, 100, 300, 500, 700, 1000]

    figsize_ratio = (3, 1)

    title_size = 22
    axis_label_size = 14
    legend_size = 10
    size_subplots_mult = 3

    fig, axs = plt.subplots(nrows=1,
                            ncols=6,
                            figsize=[x * size_subplots_mult for x in figsize_ratio],
                            sharey='all',
                            sharex='all',
                            tight_layout=True)
    fig.suptitle('Average MSE', fontsize=title_size, color='white')  # Creates space for the legends
    fig.supxlabel('Function Evaluations')
    fig.supylabel('Average MSE')

    for vertex in vertices:
        v_idx = vertices.index(vertex)
        for image in images:
            df = pd.read_csv(f'{ANALYSIS_DIR}/{vertex}/average_mse_sa/{image}.csv')
            axs[v_idx].plot(df[columns[0]], df[columns[1]], alpha=0.9)
            axs[v_idx].set_yscale('log')
            axs[v_idx].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
            axs[v_idx].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
            axs[v_idx].spines['top'].set_visible(False)
            axs[v_idx].spines['right'].set_visible(False)
            axs[v_idx].set_title(f'{vertex} Vertices')

        if v_idx == 0:
            pretty_legends = format_legends(images)
            fig.legend(pretty_legends, frameon=False, loc='center',
                       ncol=len(pretty_legends), columnspacing=0.5, bbox_to_anchor=(0.5, 0.97))

    plt.savefig(f'{ANALYSIS_DIR}/fig/average_mse_sa_good.png', bbox_inches='tight')
    plt.show()


def plot_long_mse() -> None:
    csv = 'results/others/results_starry_night.csv'

    fig, axs = plt.subplots()
    df = pd.read_csv(csv, usecols=['Iteration', 'Average MSE'])

    axs.plot(df['Iteration'], df['Average MSE'])

    plt.show()


def plot_mse() -> None:
    algo_mapping = {
        'sa': {'title': 'Simulated\nannealing', 'ylim': (125, 80000), 'yscale': 'log'},
        'hc': {'title': 'Hill\nclimber', 'ylim': (50, 16000), 'yscale': 'log'},
        'ppa': {'title': 'Plant\npropagation', 'ylim': (500, 15000), 'yscale': 'log'}
    }
    best_runs = find_best_run()
    pprint.pp(best_runs)
    count_algos = len(best_runs)
    algos = list(best_runs.keys())
    count_vertices = max([len(x) for x in best_runs.values()])
    vertices = sorted([x for x in best_runs.values()][0].keys(), key=lambda x: int(x))
    fig, axs = plt.subplots(count_algos, count_vertices, sharex='all', sharey='row')
    legends = []
    for vertex in range(count_vertices):
        for algo in range(count_algos):
            columns = ['Iteration', 'Average MSE'] if algos[algo] != 'ppa' else ['Iteration', 'Best MSE']
            dir_ = best_runs[algos[algo]][vertices[vertex]][0]
            if len([x for x in os.listdir(dir_) if x.endswith('csv')]) < 7:
                print(dir_)
            for f in sorted(os.listdir(dir_)):
                pretty_f = f.removeprefix('results_').removesuffix('.csv')
                if not f.endswith('.csv'):
                    continue
                if pretty_f not in legends:
                    legends.append(pretty_f)
                df = pd.read_csv(f'{dir_}/{f}', usecols=columns)
                axs[algo][vertex].plot(df[columns[0]], df[columns[1]])
                axs[algo][vertex].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                axs[algo][vertex].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                if algo == 0:
                    axs[algo][vertex].set_title(f'{vertices[vertex]} v.')
                if vertex == 0:
                    axs[algo][vertex].set_ylabel(algo_mapping[algos[algo]]['title'])
                axs[algo][vertex].spines['top'].set_visible(False)
                axs[algo][vertex].spines['right'].set_visible(False)

    fig.legend(format_legends(legends), frameon=False, loc='center',
               ncol=len(legends), columnspacing=1, bbox_to_anchor=(0.533, 0.99))

    plt.show()


def plot_mse_distribution() -> None:
    freq_array = pd.read_pickle('results/log/1000/1_ppa_ffa/list_bach.pkl')

    fig, axs = plt.subplots()
    n, bins, patches = axs.hist(freq_array, bins=100)
    fracs = n / n.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.set_title('Run 1 - Bach - 1000 vertices - PPA', fontsize=15)
    axs.set_xlabel('MSE', fontdict={'size': 15})
    axs.set_ylabel('Frequency', fontdict={'size': 15})
    axs.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
    axs.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
    axs.set_xlim(None, 32500)

    plt.plot()
    plt.savefig('results/analysis/fig/mse_distribution.png')
    plt.show()


def find_best_mse() -> None:
    dict_ = {}

    for vertices in os.listdir(LOG_DIR):
        for dir_ in os.listdir(f'{LOG_DIR}/{vertices}'):
            info = dir_.split('_')
            if info[-1] != 'ffa':
                continue
            algo = info[1]

            if algo not in dict_:
                dict_[algo] = {}

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            for csv in os.listdir(f'{LOG_DIR}/{vertices}/{dir_}'):
                if 'plot' in csv or csv.endswith('pkl'):
                    continue
                name = csv.removeprefix("results_").removesuffix(".csv")
                mse_col = 'Average MSE' if algo != 'ppa' else 'Best MSE'

                if name not in dict_[algo][vertices]:
                    dict_[algo][vertices][name] = int(pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].min())

                else:
                    current_value = dict_[algo][vertices][name]
                    new_value = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1].min()
                    if new_value < current_value:
                        dict_[algo][vertices][name] = int(new_value)

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        df.to_csv(f'{ANALYSIS_DIR}/best_mse_{algo}_ffa.csv', index_label='vertices')


if __name__ == '__main__':
    # average_runs_mse()
    graph_average_mse()
    # plot_mse()
    # plot_new_sa()
    # plot_mse_distribution()
    # plot_long_mse()
    # find_best_mse()

# Plots: choose best run based on average last MSE of all paintings for all permutations of algos and vertices:
# 3 * 6 = 18 plots
