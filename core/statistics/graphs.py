import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

ANALYSIS_DIR = 'results/analysis'
LOG_DIR = 'results/log'


def graph_average_mse() -> None:
    vertices = [20, 100, 300, 500, 700, 1000]
    algos = ['hc', 'ppa', 'sa']
    algo_mapping = {
        'sa': {'title': 'Simulated annealing', 'ylim': (125, 80000), 'yscale': 'log'},
        'hc': {'title': 'Hill climber', 'ylim': (50, 16000), 'yscale': 'log'},
        'ppa': {'title': 'Plant propagation', 'ylim': (500, 15000), 'yscale': 'log'}
    }
    figsize_ratio = (2.5, 3)
    columns = ['Iteration', 'Average MSE']

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
            average_dir = f'{ANALYSIS_DIR}/{vertice}/average_mse_{algo}/'

            if not os.path.exists(f'{ANALYSIS_DIR}/fig/{vertice}'):
                os.makedirs(f'{ANALYSIS_DIR}/fig/{vertice}', exist_ok=True)

            for count_a, ax in enumerate(axs):
                if count_a == count_v:
                    ax.set_ylim(algo_mapping[algo]['ylim'])
                    ax.set_yscale(algo_mapping[algo]['yscale'])

                    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
                    if ax.get_yscale() == 'linear':
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))

                    if algos.index(algo) == 0:
                        ax.set_title(f"{vertice} vert.")

                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)

                    legends = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
                               'the_persistence_of_memory']
                    if count_a == 0:
                        pretty_legends = format_legends(legends)
                        fig.legend(pretty_legends, frameon=False, fontsize=legend_size, loc='center',
                                   ncol=len(pretty_legends), columnspacing=1, bbox_to_anchor=(0.5, 0.99))

                    for image in legends:
                        df = pd.read_csv(f'{average_dir}{image}.csv', usecols=columns)
                        ax.plot(df[columns[0]], df[columns[1]],
                                label=image)

    plt.plot()
    plt.savefig(f"{ANALYSIS_DIR}/fig/average_mse.png", bbox_inches='tight', format='png')
    plt.show()


def graph_best_mse() -> None:
    csvs = [dir_ for dir_ in os.listdir(ANALYSIS_DIR) if dir_.endswith('.csv') and 'best_mse' in dir_]
    algos = ['hc', 'ppa', 'sa']
    studies = ['Replication study', 'Original study']
    algo_mapping = {
        'sa': {'title': 'Simulated annealing', 'ylim': (14000, 80000), 'yscale': 'linear'},
        'hc': {'title': 'Hill climber', 'ylim': (50, 16000), 'yscale': 'log'},
        'ppa': {'title': 'Plant propagation', 'ylim': (500, 15000), 'yscale': 'log'}
    }

    title_size = 22
    figsize_ratio = (2.5, 3)
    size_subplots_mult = 3
    legend_size = 10

    plt.style.use('default')
    fig = plt.figure(figsize=tuple([x * size_subplots_mult for x in figsize_ratio]), constrained_layout=True)
    subfigs = fig.subfigures(3, 1)
    fig.suptitle('Average MSE', fontsize=title_size, color='white')  # Creates space for the legends
    fig.supylabel('Best MSE', weight='bold')
    fig.supxlabel('Vertices', weight='bold')

    for algo in algos:
        axs = subfigs[algos.index(algo)].subplots(ncols=2, sharex='all', sharey='row')
        subfigs[algos.index(algo)].supylabel(algo_mapping[algo]['title'])

        for count, ax in enumerate(axs):
            csvs_avail = [csv for csv in csvs if algo in csv]
            df = pd.read_csv(f'{ANALYSIS_DIR}/{csvs_avail[count]}', index_col=0)

            if (count == 0 and algos.index(algo) == 0) or (count == 1 and algos.index(algo) == 0):
                ax.set_title(f'{studies[count]}')

            if algo != 'sa':
                ax.set_yscale('log')
            ax.plot(df, marker='o', markersize=3)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            if ax.get_yscale() == 'linear':
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))

            if count == 0 and algos.index(algo) == 0:
                legends = format_legends(['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
                                          'the_persistence_of_memory'])
                fig.legend(format_legends(legends), fontsize=legend_size, loc='center', ncol=len(legends),
                           frameon=False, columnspacing=0.5, bbox_to_anchor=(0.533, 0.99))

    plt.plot()
    plt.savefig(f"{ANALYSIS_DIR}/fig/best_mse_comp.png", bbox_inches='tight', format='png')
    plt.show()


def average_runs_mse() -> None:
    for algo in ['sa', 'ppa', 'hc']:
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


def graph_mse_distribution() -> None:
    df = pd.read_pickle(f'results/others/mapping_bach.pkl')
    lst = []
    for key, value in df.items():
        for _ in range(value):
            lst.append(key)
    fig, ax = plt.subplots()
    ax.hist(lst, bins=50)
    plt.show()


def graph_ffa() -> None:
    df = pd.read_csv(f'results/others/results_bach.csv', usecols=['Iteration', 'Average MSE'])
    fig, ax = plt.subplots()
    ax.plot(df['Iteration'], df['Average MSE'])
    plt.show()


def find_best_mse() -> None:
    dict_ = {}

    for vertices in os.listdir(LOG_DIR):
        for dir_ in os.listdir(f'{LOG_DIR}/{vertices}'):
            info = dir_.split('_')
            if info[-1] == 'ffa':
                continue
            algo = info[1]
            if algo != 'sa':
                continue

            if algo not in dict_:
                dict_[algo] = {}

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            for csv in os.listdir(f'{LOG_DIR}/{vertices}/{dir_}'):
                if 'plot' in csv or csv.endswith('.pkl'):
                    continue
                name = csv.removeprefix("results_").removesuffix(".csv")
                mse_col = 'Average MSE' if algo != 'ppa' else 'Best MSE'

                if name not in dict_[algo][vertices]:
                    dict_[algo][vertices][name] = int(pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1])

                else:
                    current_value = dict_[algo][vertices][name]
                    new_value = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1]
                    if new_value < current_value:
                        dict_[algo][vertices][name] = int(new_value)

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        df.to_csv(f'{ANALYSIS_DIR}/best_mse_{algo}.csv', index_label='vertices')


def find_avg_mse() -> None:
    dict_ = {}

    for vertices in os.listdir(LOG_DIR):
        for dir_ in os.listdir(f'{LOG_DIR}/{vertices}'):
            if dir_.endswith('_ffa'):
                continue
            algo = dir_.split('_')[-1]
            run = dir_.split('_')[0]

            if algo not in dict_:
                dict_[algo] = {}

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            for csv in os.listdir(f'{LOG_DIR}/{vertices}/{dir_}'):
                name = csv.removeprefix("results_").removesuffix(".csv")
                mse_col = 'Average MSE'

                if name not in dict_[algo][vertices]:
                    dict_[algo][vertices][name] = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1]

                else:
                    new_value = pd.read_csv(f'{LOG_DIR}/{vertices}/{dir_}/{csv}')[mse_col].iloc[-1]
                    dict_[algo][vertices][name] += new_value

                    if run == '5':
                        dict_[algo][vertices][name] /= 5
                        dict_[algo][vertices][name] = str(int(dict_[algo][vertices][name]))

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        df.to_csv(f'{ANALYSIS_DIR}/avg_mse_{algo}.csv', index_label='vertices')


def find_avg_mse_other() -> None:
    dict_ = {}

    for file in os.listdir(f'{LOG_DIR}/other'):
        algo = file.split('-')[0].lower()

        if algo not in dict_:
            dict_[algo] = {}

        df = pd.read_csv(f'{LOG_DIR}/other/{file}')

        for index, row in df.iterrows():
            vertices = row['Vertices']
            image = row['Painting']

            if image == 'dali':
                image = 'the_persistence_of_memory'
            elif image == 'monalisa':
                image = 'mona_lisa'
            elif image == 'mondriaan2':
                image = 'mondriaan'
            elif image == 'pollock':
                image = 'convergence'
            elif image == 'starrynight':
                image = 'starry_night'
            elif image == 'kiss':
                image = 'the_kiss'

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            if image not in dict_[algo][vertices]:
                dict_[algo][vertices][image] = row['MSE']
            else:
                dict_[algo][vertices][image] += row['MSE']

        for vertices in dict_[algo]:
            for image in dict_[algo][vertices]:
                dict_[algo][vertices][image] /= 5
                dict_[algo][vertices][image] = str(int(dict_[algo][vertices][image]))

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        if len(df.columns.values) == 6:
            df = df[['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night',
                     'the_persistence_of_memory']]
        else:
            df = df[['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
                     'the_persistence_of_memory']]
        df.to_csv(f'{ANALYSIS_DIR}/avg_mse_{algo}_other.csv', index_label='vertices')


def find_best_mse_other() -> None:
    dict_ = {}

    for file in os.listdir(f'{LOG_DIR}/other'):
        algo = file.split('-')[0].lower()

        if algo not in dict_:
            dict_[algo] = {}

        df = pd.read_csv(f'{LOG_DIR}/other/{file}')

        for index, row in df.iterrows():
            vertices = row['Vertices']
            image = row['Painting']

            if image == 'dali':
                image = 'the_persistence_of_memory'
            elif image == 'monalisa':
                image = 'mona_lisa'
            elif image == 'mondriaan2':
                image = 'mondriaan'
            elif image == 'pollock':
                image = 'convergence'
            elif image == 'starrynight':
                image = 'starry_night'
            elif image == 'kiss':
                image = 'the_kiss'

            if vertices not in dict_[algo]:
                dict_[algo][vertices] = {}

            if image not in dict_[algo][vertices]:
                dict_[algo][vertices][image] = row['MSE']
            else:
                new_mse = row['MSE']
                if new_mse > dict_[algo][vertices][image]:
                    dict_[algo][vertices][image] = new_mse

        for vertices in dict_[algo]:
            for image in dict_[algo][vertices]:
                dict_[algo][vertices][image] = str(int(dict_[algo][vertices][image]))

    for algo in dict_:
        df = pd.DataFrame(dict_[algo]).T
        df = df.reindex(sorted(df.index, key=lambda x: int(x)))
        if len(df.columns.values) == 6:
            df = df[['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night',
                     'the_persistence_of_memory']]
        else:
            df = df[['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss',
                     'the_persistence_of_memory']]
        df.to_csv(f'{ANALYSIS_DIR}/best_mse_{algo}_other.csv', index_label='vertices')


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


def format_number(data_value: float) -> str:
    if data_value == 0:
        return '0'
    if data_value >= 1000000:
        formatter = '{:1.0f}M'.format(data_value * 0.000001)
    else:
        formatter = '{:1.0f}K'.format(data_value * 0.001)
    return formatter


if __name__ == '__main__':
    pass
    # find_best_mse()
    # graph_best_mse()

    # average_runs_mse()
    # find_avg_mse()
    # graph_average_mse()

    # find_avg_mse_other()
    # find_best_mse_other()

    # graph_ffa()
    # graph_mse_distribution()
