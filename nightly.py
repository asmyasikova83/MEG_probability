import argparse
from test import check_ga, check_tfr, test

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=['full_ERF', 'full_TFR'], help='long tests: ERF and TFR')
    args = parser.parse_args()
    name = args.name
    stages = ['events', 'mio']
    if name == 'full_ERF':
        mode = 'ga'
        stages += ['ERF']
        check_func = check_ga
    elif name == 'full_TFR':
        mode = 'tfr'
        stages += ['tfr', 'contaner_tfr']
        check_func = check_tfr
    stages += ['tfce']
    test(name, mode, stages, [], [], check_func)
