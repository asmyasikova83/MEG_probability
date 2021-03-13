import os
import shutil
import argparse
from datetime import datetime

import config
from risk_norisk_events_extraction import risk_norisk_events
from mio_correction import mio_correction

from grand_average import grand_average_process
from tfr import tfr_process
from make_evoked_freq_data_container import container_process

from tfce_time_course_in_html_call import tfce_process
from make_pdf_from_pic_and_html_time_course import make_pdf

from plot_topo_stat_call import topo_stat
from plot_topo_fdr_pdf import make_fdr_pdf

def env(path, prev_path=None):
    if prev_path:
        assert os.path.exists(prev_path) and os.path.isdir(prev_path), f"{prev_path} does not exist"
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok = True)

def run(mode, stages=None, work_dir='WORK/', test_prefix='run', add_date=False, verbose=False):
    if add_date:
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
        subdir_name = test_prefix + '__' + dt_string + '/'
        work_dir += subdir_name
    else:
        work_dir += test_prefix + '/'

    run_events_extraction = False
    run_mio_correction = False

    run_grand_average = False
    run_tfr = False
    run_container = False

    run_tfce = False
    convert_pdf = False

    run_fdr = False
    convert_fdr_pdf = False

    if mode == 'ga':
        conf = config.conf(mode = 'grand_average', kind = ['norisk', 'risk'], work_dir = work_dir, verbose = verbose)
    elif mode == 'tfr':
        conf = config.conf(mode = 'tfr', kind = ['norisk', 'risk'], frequency = 'theta', work_dir = work_dir, verbose = verbose)

    if not stages:
        print('All stages!')
        run_events_extraction = True
        run_mio_correction = True

        if mode == 'ga':
            run_grand_average = True
        elif mode == 'tfr':
            run_tfr = True
            run_container = True

        run_tfce = True
        convert_pdf = True

        run_fdr = True
        convert_fdr_pdf = True

    else:
        for stage in stages:
            if stage == 'events':
                run_events_extraction = True
            elif stage == 'mio':
                run_mio_correction = True

            elif stage == 'ERF':
                assert mode == 'ga'
                run_grand_average = True
            elif stage == 'tfr':
                assert mode == 'tfr'
                run_tfr = True
            elif stage == 'container_tfr':
                assert mode == 'tfr'
                run_container = True

            elif stage == 'tfce':
                run_tfce = True
            elif stage == 'tfce_pdf':
                convert_pdf = True

            elif stage == 'fdr':
                run_fdr = True
            elif stage == 'fdr_pdf':
                convert_fdr_pdf = True

    if run_events_extraction:
        env(conf.path_events)
        risk_norisk_events(conf)

    if run_mio_correction:
        env(conf.path_mio, conf.path_events)
        mio_correction(conf)

    if mode == 'ga':
        if run_grand_average:
            env(conf.path_GA, conf.path_mio)
            grand_average_process(conf)
    else:
        if run_tfr:
            env(conf.path_tfr, conf.path_mio)
            tfr_process(conf)
        print(run_container)
        if run_container:
            env(conf.path_container, conf.path_tfr)
            container_process(conf)


    if run_tfce:
        env(conf.path_tfce, conf.path_GA if mode == 'ga' else conf.path_container)
        tfce_process(conf)

    if convert_pdf:
        env(conf.path_pdf, conf.path_tfce)
        make_pdf(conf)


    if run_fdr:
        env(conf.path_fdr, conf.path_GA if mode == 'ga' else conf.path_container)
        topo_stat(conf)

    if convert_fdr_pdf:
        env(conf.path_fdr_pdf, conf.path_fdr)
        make_fdr_pdf(conf)

    # return dir to check
    return conf.prefix_out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['ga', 'tfr'], help='available modes: ga(aka grand_average), tfr')
    parser.add_argument('-s', '--stage', \
        choices=['events', 'mio', 'ERF', 'tfr', 'container_tfr', 'tfce', 'tfce_pdf', 'fdr', 'fdr_pdf'], \
        help='stage of processing')
    args = parser.parse_args()
    mode = args.mode
    stage = args.stage

    run(mode, None if not stage else [stage])
