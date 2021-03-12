import difflib
import sys
import os

from run import run

def check(out_file, ref_file):
    res = True
    with open(out_file, 'r') as out:
        with open(ref_file, 'r') as ref:
            diff = difflib.unified_diff(
                    out.readlines(),
                    ref.readlines(),
                    fromfile=out_file,
                    tofile=ref_file
                    )
    for line in diff:
        print(line)
        res = False
    return res

def check_ga_tstat(out_path, ref_path):
    f = 'TFCE/GA/t_stat_norisk_vs_risk.txt'
    out_file = out_path + f
    ref_file = ref_path + f
    return check(out_file, ref_file)

def check_events(out_path, ref_path):
    res = True
    events = 'events'
    out_events = out_path + events
    ref_events = ref_path + events
    out_names = os.listdir(out_events)
    ref_names = os.listdir(ref_events)
    for ref_name in ref_names:
        found = False
        if ref_name in out_names:
            found = True
            res = res and check(out_events + '/' + ref_name, ref_events + '/' + ref_name)
        if not found:
            print('Cannot find', ref_name)
            return False
    return res

def test(test_name, mode, stage, check_func):
    print('Run test:', test_name)
    cur_dir = os.getcwd()
    out_path = run(mode, stage, work_dir='TEST/', test_prefix=test_name, add_date=True)
    os.chdir(cur_dir)
    check_result = check_func(out_path, 'ref/' + test_name + '/')
    if check_result:
        print('Test %s passed\n' % test_name)
    else:
        print('Test %s failed\n' % test_name)
        assert 0

test('test1_events', 'ga', 'events', check_events)
test('test2_tstat', 'ga', None, check_ga_tstat)
 
