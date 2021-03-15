import argparse
from run import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=['full_ERF', 'full_TFR'], help='long run: ERF and TFR')
    args = parser.parse_args()
    name = args.name
    if name == 'full_ERF':
        mode = 'ga'
        prefix = 'ERF'
    elif name == 'full_TFR':
        mode = 'tfr'
        prefix = 'TFR'
    run(mode,  None, [], [], work_dir='COLLECT/', test_prefix=prefix, add_date=True)

