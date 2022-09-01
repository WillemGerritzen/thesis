import math
import os
import shutil

import pandas as pd
from numpy import arange
from pandas import Index


def move_bad_sa():
    gen = os.walk('results/log')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if 'sa' in x]
    for sa_dir in sa_dirs:
        shutil.move(sa_dir, 'results/log/others/bad_sa/' + sa_dir.removeprefix('results/log/'))


def remove_bad_sa():
    gen = os.walk('results/log')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if '_ffa' in x]
    for sa_dir in sa_dirs:
        shutil.rmtree(sa_dir)


def move_good_sa():
    gen = os.walk('results/log/')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if 'ffa' in x]
    for sa_dir in sa_dirs:
        print(sa_dir)
        for f in os.listdir(sa_dir):
            if f.endswith('plot_plot.csv'):
                os.remove(sa_dir + '/' + f)
        # shutil.move(sa_dir, 'results/log/' + sa_dir.removeprefix('results/log/log/'))


def remove_ffa_dirs():
    gen = os.walk('results/log')
    dirs = [x[0] for x in gen]
    ffa_dirs = [x for x in dirs if ('ppa_ffa' in x) and ('700' in x or '1000' in x)]
    for ffa_dir in ffa_dirs:
        shutil.rmtree(ffa_dir)


def start_uncompleted_jobs():
    runs = range(1, 6)
    vertices = [20, 100, 300, 500, 700, 1000]
    images = ['bach', 'convergence', 'the_persistence_of_memory', 'mona_lisa', 'mondriaan', 'the_kiss', 'starry_night']
    algos = ['hc', 'ppa', 'sa']
    FFA = '--ffa'
    dump_dir = 'thesis/dump/log/'
    gen = os.walk(dump_dir)
    dirs = [x[0] for x in gen]
    for dir in dirs:
        if not dir.endswith('_sa_ffa'):
            continue
        for file in os.listdir(dir):
            if file.endswith('.csv') and not 'list_{image}.pkl'.format(image=file[8:-4]) in os.listdir(dir):
                csv = '{dir}/results_{image}.csv'.format(dir=dir, image=file[8:-4])
                print('Found {csv} with no corresponding pickle, removing...'.format(csv=csv))
                # os.remove(csv)
                split_dir = dir.split('/')
                vertices = split_dir[3]
                run = split_dir[-1].split('_')[0]
                algo = split_dir[-1].split('_')[1]
                image = csv.split('_')[-1][:-4]
                name = '{run}_{algo}_{image}_{vertices}{FFA}'.format(run=run, algo=algo, image=image, vertices=vertices, FFA=FFA)
                print('Starting job for {name}'.format(name=name))
                # os.system('cd job_logs && sbatch -J {name} job.sh {algo} {run} {image} {vertices} {FFA}'.format(
                #     name=name, algo=algo, run=run, image=image, vertices=vertices, FFA=FFA))

def start_missing_jobs():
    runs = range(1, 6)
    vertices = [20, 100, 300, 500, 700, 1000]
    images = ['bach', 'convergence', 'the_persistence_of_memory', 'mona_lisa', 'mondriaan', 'the_kiss', 'starry_night']
    algos = ['hc', 'ppa', 'sa']
    FFA = '--ffa'
    dump_dir = 'thesis/dump/log/'
    gen = os.walk(dump_dir)
    dirs = [x[0] for x in gen]
    for dir in dirs:
        if 'ffa' not in dir:
            continue
        for image in images:
            file = 'results_{image}.csv'.format(image=image)
            if file not in os.listdir(dir):
                split_dir = dir.split('/')
                vertices = split_dir[3]
                run = split_dir[-1].split('_')[0]
                algo = split_dir[-1].split('_')[1]
                name = '{run}_{algo}_{image}_{vertices}{FFA}'.format(run=run, algo=algo, image=image, vertices=vertices,
                                                                     FFA=FFA)
                print('Starting job for {name}'.format(name=name))
                # os.system('cd job_logs && sbatch -J {name} job.sh {algo} {run} {image} {vertices} {FFA}'.format(
                #     name=name, algo=algo, run=run, image=image, vertices=vertices, FFA=FFA))


def cancel_bad_jobs():
    runs = range(1, 6)
    vertices = [20, 100, 300, 500, 700, 1000]
    images = ['bach', 'convergence', 'the_persistence_of_memory', 'mona_lisa', 'mondriaan', 'the_kiss', 'starry_night']
    algos = ['hc', 'ppa', 'sa']
    FFA = '--ffa'
    for run in runs:
        for image in images:
            job = '{run}_sa_{image}_1000--ffa'.format(run=run, image=image)
            os.system('scancel -u gerritzen -n {job}'.format(job=job))
            # print(job)


def check_all_jobs():
    runs = range(1, 6)
    vertices = [20, 100, 300, 500, 700, 1000]
    images = ['bach', 'convergence', 'the_persistence_of_memory', 'mona_lisa', 'mondriaan', 'the_kiss', 'starry_night']
    algos = ['hc', 'ppa', 'sa']
    FFA = '_ffa'
    log_dir = f'results/log'
    # dir_lst = pickle.load(open('dir_list.pkl', 'rb'))
    # print(dir_lst)
    for run in runs:
        for vertex in vertices:
            for image in images:
                for algo in algos:
                    if algo != 'sa':
                        continue
                    csv = f'{log_dir}/{vertex}/{run}_{algo}/results_{image}.csv'
                    if not os.path.exists(csv):
                        print(csv)

                    # check = '{dump_dir}/{vertex}/{run}_{algo}_ffa/{image}.pkl'.format(
                    #     dump_dir=dump_dir, vertex=vertex, run=run, algo=algo, image=image)
                    # pkl = '{dump_dir}/{vertex}/{run}_{algo}_ffa/list_{image}.pkl'.format(
                    #     dump_dir=dump_dir, vertex=vertex, run=run, algo=algo, image=image)
                    # csv = f'{dump_dir}/{vertex}/{run}_{algo}_ffa/results_{image}.csv'
                    # if check in dir_lst and os.path.exists(pkl) and os.path.exists(csv):
                    #     print(csv)
                        # dir_lst.append('{dump_dir}/{vertex}/{run}_{algo}_ffa/{image}.pkl'.format(
                        #     dump_dir=dump_dir, vertex=vertex, run=run, algo=algo, image=image))
    # with open('thesis/dir_list.pkl', "wb") as f:
    #     pickle.dump(dir_lst, f)


def transform_mse_frequency() -> None:
    log_dir = 'results/log/'
    for vertices_dir_ in os.listdir(log_dir):
        for dir_ in os.listdir(log_dir + vertices_dir_):
            if 'ffa' not in dir_:
                continue
            for f in os.listdir(log_dir + vertices_dir_ + '/' + dir_):
                if f.endswith('pkl') or 'plot' in f:
                    continue
                transform_file(log_dir + vertices_dir_ + '/' + dir_ + '/' + f)


def transform_file(f) -> None:
    lst = []
    columns = ['Iteration', 'Average MSE'] if 'ppa' not in f else ['Iteration', 'Best MSE']
    df = pd.read_csv(f, usecols=columns)
    for x in df.iterrows():
        y = int(math.ceil(x[1]['Iteration'] / 1000.0)) * 1000
        lst.append(y)
    df1 = df.copy()
    df1['Iteration'] = lst
    df1.drop_duplicates(subset='Iteration', inplace=True, keep='last')
    new_index = Index(arange(0, 1000001, 1000), name="Iteration")
    df1 = df1.set_index("Iteration").reindex(new_index).reset_index()
    df1 = df1.fillna(method='ffill')
    df1['Iteration'].iloc[1000] = 999999
    df1 = df1.set_index("Iteration")
    df1 = df1.rename(columns={columns[1]: 'MSE'})
    if df1['MSE'].iloc[1000] > df1['MSE'].iloc[999]:
        print(df1['MSE'].iloc[1000], df1['MSE'].iloc[999])
        df1['MSE'].iloc[1000] = df1['MSE'].iloc[999]
    df1.to_csv(f[:-4] + '_plot.csv')


if __name__ == '__main__':
    # move_bad_sa()
    # move_good_sa()
    # remove_bad_sa()

    # remove_ffa_dirs()
    # print('Incomplete jobs:')
    # start_uncompleted_jobs()
    # print('Missing jobs:')
    # start_missing_jobs()
    # cancel_bad_jobs()
    check_all_jobs()
    # transform_mse_frequency()
