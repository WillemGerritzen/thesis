import os
import shutil


def move_bad_sa() -> None:
    gen = os.walk('results/log')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if 'sa' in x]
    for sa_dir in sa_dirs:
        shutil.move(sa_dir, 'results/log/others/bad_sa/' + sa_dir.removeprefix('results/log/'))


def remove_bad_sa() -> None:
    gen = os.walk('results/log')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if 'sa' in x]
    for sa_dir in sa_dirs:
        shutil.rmtree(sa_dir)

def move_good_sa() -> None:
    gen = os.walk('results/log/log/')
    dirs = [x[0] for x in gen]
    sa_dirs = [x for x in dirs if 'sa' in x]
    for sa_dir in sa_dirs:
        shutil.move(sa_dir, 'results/log/' + sa_dir.removeprefix('results/log/log/'))
        # print(sa_dir.removeprefix('results/log/log/'))


if __name__ == '__main__':
    # move_bad_sa()
    # move_good_sa()
    remove_bad_sa()
