import argparse
from test import check_ga, check_tfr, test

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=['full_ERF', 'full_TFR'], help='long tests: ERF and TFR')
    args = parser.parse_args()
    name = args.name
    if name == 'full_ERF':
        mode = 'ga'
        check_func = check_ga
    elif name == 'full_TFR':
        mode = 'tfr'
        check_func = check_tfr
    test(name, mode, None, [], [], check_func)
