import pandas as pd

ANALYSIS_DIR = '../../results/analysis'

def improvement() -> None:
    dict_ = {}
    algos = ['hc', 'ppa', 'sa']
    vertices = [20, 100, 300, 500, 700, 1000]
    images = ['bach', 'convergence', 'mona_lisa', 'mondriaan', 'starry_night', 'the_kiss', 'the_persistence_of_memory']

    for algo in algos:
        if not dict_.get(algo):
            dict_[algo] = {}
        df = pd.read_csv(f'{ANALYSIS_DIR}/avg_mse_{algo}_ffa.csv')
        for image in images:
            dict_[algo][image] = max(df[image]) - min(df[image])
    df1 = pd.DataFrame(dict_).T
    df1.to_csv(f'{ANALYSIS_DIR}/imp_ffa.csv')



if __name__ == '__main__':
    improvement()
