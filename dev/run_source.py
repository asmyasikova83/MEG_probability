import os
import shutil
import argparse
from datetime import datetime

import config
from risk_norisk_events_extraction import risk_norisk_events
from mio_correction import mio_correction

from source import source_process

def env(path, prev_path=None):
    if prev_path:
        assert os.path.exists(prev_path) and os.path.isdir(prev_path), f"{prev_path} does not exist"
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok = True)

def run(mode, stages, subjects, runs, work_dir='WORK/', test_prefix='run', add_date=False, verbose=False):
    if add_date:
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
        subdir_name = test_prefix + '__' + dt_string + '/'
        work_dir += subdir_name
    else:
        work_dir += test_prefix + '/'

    run_events_extraction = False
    run_mio_correction = False

    run_source = False


    if mode == 'source':
        conf = config.conf(mode='source', kind=['norisk', 'risk'],
                subjects=subjects, runs=runs, frequency = 'theta', work_dir=work_dir, verbose=True)
    #elif mode == 'tfr':
    #    conf = config.conf(mode='tfr', kind=['norisk', 'risk'],
    #            subjects=subjects, runs=runs, frequency='theta', work_dir=work_dir, verbose=verbose)
    else:
        assert 0, 'Wrong mode'

    if not stages:
        print('All stages!')
        run_events_extraction = True
        run_mio_correction = True

        if mode == 'source':
            run_source = True
        #elif mode == 'tfr':
        #    run_tfr = True
        #    run_container = True

    else:
        for stage in stages:
            if stage == 'events':
                run_events_extraction = True
            elif stage == 'mio':
                run_mio_correction = True

            elif stage == 'source':
                assert mode == 'source'
                run_source = True

    if run_events_extraction:
        env(conf.path_events)
        risk_norisk_events(conf)

    if run_mio_correction:
        env(conf.path_mio, conf.path_events)
        mio_correction(conf)

    if run_source:
        env(conf.path_source, conf.path_mio)
        source_process(conf)

    # return dir to check
    return conf.prefix_out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['source'], help='available modes: source')
    parser.add_argument('-s', '--stage', \
        choices=['events', 'mio'], \
        help='stage of processing')
    args = parser.parse_args()
    if mode == 'source':
        subjects = ['P011']
        runs = ['2']
    stage = args.stage

    run(mode, None if not stage else [stage], subjects, runs)
