import os

import matplotlib.pyplot as plt
import pandas as pd

from core.statistics.graphs import format_legends, format_number

ANALYSIS_DIR = 'results/analysis'
LOG_DIR = 'results/log'


# def graph_average_mse() -> None:
#     vertices = [20, 100, 300, 500, 700, 1000]
#     algos = ['hc', 'ppa', 'sa']
#     algo_mapping = {
#         'sa': {'title': 'Simulated annealing'},
#         'hc': {'title': 'Hill climber'},
#         'ppa': {'title': 'Plant propagation'}
#     }
#     figsize_ratio = (2.5, 3)
#     columns = ['Iteration', 'Average MSE']
#
#     title_size = 22
#     axis_label_size = 14
#     legend_size = 10
#     size_subplots_mult = 3.2
#
#     plt.style.use('default')
#     fig = plt.figure(figsize=tuple([x * size_subplots_mult for x in figsize_ratio]), constrained_layout=True)
#     subfigs = fig.subfigures(3, 1)
#     fig.suptitle('Average MSE', fontsize=title_size, color='white')  # Creates space for the legends
#     fig.supxlabel('Function Evaluations', size=axis_label_size, weight='bold')
#     fig.supylabel('Average MSE', size=axis_label_size, weight='bold')
#
#     for algo in algos:
#         axs = subfigs[algos.index(algo)].subplots(ncols=len(vertices), sharex=True, sharey=True)
#         subfigs[algos.index(algo)].supylabel(algo_mapping[algo]['title'])
#
#         for count_v, vertice in enumerate(vertices):
#             average_dir = f'{ANALYSIS_DIR}/{vertice}/average_mse_{algo}_ffa/'
#
#             if not os.path.exists(f'{ANALYSIS_DIR}/fig/{vertice}'):
#                 os.makedirs(f'{ANALYSIS_DIR}/fig/{vertice}', exist_ok=True)
#
#             for count_a, ax in enumerate(axs):
#                 # if count_a == count_v:
#                 #     ax.set_ylim(algo_mapping[algo]['ylim'])
#                 #     ax.set_yscale(algo_mapping[algo]['yscale'])
#
#                 ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
#                 if ax.get_yscale() == 'linear':
#                     ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
#
#                 if algos.index(algo) == 0:
#                     ax.set_title(f"{vertice} Vert.")
#
#                 ax.spines['top'].set_visible(False)
#                 ax.spines['right'].set_visible(False)
#
#                 legends = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
#                            'the_persistence_of_memory']
#                 if count_a == 0:
#                     pretty_legends = format_legends(legends)
#                     fig.legend(pretty_legends, frameon=False, fontsize=legend_size, loc='center',
#                                ncol=len(pretty_legends), columnspacing=1, bbox_to_anchor=(0.533, 0.99))
#
#                 for image in legends:
#                     df = pd.read_csv(f'{average_dir}{image}.csv', usecols=columns)
#                     ax.plot(df[columns[0]], df[columns[1]],
#                             label=image)
#
#     plt.plot()
#     # plt.savefig(f"{ANALYSIS_DIR}/fig/average_mse.png", bbox_inches='tight', format='png')
#     plt.show()

def plot_mse() -> None:
    runs = range(1, 5)
    algos = ['ppa', 'sa', 'hc']
    images = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
              'the_persistence_of_memory']
    pretty_images = {img: pre_img for pre_img, img in zip(format_legends(images), images)}
    for run in runs:
        fig, axs = plt.subplots(nrows=len(algos), ncols=len(images), sharex='all', sharey='row')
        fig.suptitle(f'Run {run}')
        for algo in algos:
            columns = ['Iteration', 'Average MSE'] if algo != 'ppa' else ['Iteration', 'Best MSE']
            for image in images:
                df = pd.read_csv(f'{LOG_DIR}/20/{run}_{algo}_ffa/results_{image}.csv',
                                 usecols=columns)
                axs[algos.index(algo)][images.index(image)].plot(df[columns[0]], df[columns[1]])
                axs[algos.index(algo)][images.index(image)].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                axs[algos.index(algo)][images.index(image)].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                if algos.index(algo) == 0:
                    axs[algos.index(algo)][images.index(image)].set_title(f"{pretty_images[image]}")
        plt.show()


def average_runs_mse() -> None:
    for algo in ['sa', 'ppa', 'hc']:
        for vertices in [20, 100, 300, 500, 700, 1000]:
            logs_dir = f'{LOG_DIR}/{vertices}/'
            average_dir = f'{ANALYSIS_DIR}/{vertices}/average_mse_{algo}_ffa/'

            if not os.path.exists(average_dir):
                os.makedirs(average_dir, exist_ok=True)
            else:
                for file in os.listdir(average_dir):
                    os.remove(average_dir + file)

            for dir_ in os.listdir(logs_dir):
                if dir_.split('_')[0] == 'average' or dir_.split('_')[0] == 'best':
                    continue
                if not dir_.endswith('_ffa'):
                    continue

                for csv in os.listdir(logs_dir + dir_):
                    if dir_.split('_')[1] != algo:
                        continue

                    name = csv.lower().removeprefix("results_")

                    if 'johann' in name:
                        name = name.replace('johann_sebastian_', '')

                    if not os.path.exists(average_dir + name):
                        if csv.endswith('.pkl'):
                            continue

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
    # average_runs_mse()
    # graph_average_mse()
    plot_mse()
