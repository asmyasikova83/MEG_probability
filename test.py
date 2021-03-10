import difflib
import sys
import os

from run import run

def check_dir(out_dir, ref_dir):
    res = True
    out_files = os.listdir(out_dir)
    ref_files = os.listdir(ref_dir)
    for ref_file in ref_files:
        found = False
        for out_file in out_files:
            if ref_file == out_file:
                found = True
                with open(out_dir+'/'+out_file, 'r') as out:
                    with open(ref_dir+'/'+ref_file, 'r') as ref:
                        diff = difflib.unified_diff(
                                out.readlines(),
                                ref.readlines(),
                                fromfile=out_file,
                                tofile=ref_file
                                )
                        for line in diff:
                             print(line)
                             res = False
        if not found:
            print('Cannot find', ref_name)
            return False
    return res

def check_ref(out_dir_root, test_name):
    ref_dir_root = 'ref/' + test_name
    res = True
    out_dirs = os.listdir(out_dir_root)
    ref_dirs = os.listdir(ref_dir_root)
    for ref_dir in ref_dirs:
        found = False
        if ref_dir in out_dirs:
            found = True
            res = res and check_dir(out_dir_root+'/'+ref_dir, ref_dir_root+'/'+ref_dir)
        if not found:
            print('Cannot find', ref_dir)
            return False
    return res

test_name = 'test1_events'
print('Run test:', test_name)
work_dir = run('ga', 'events', work_dir='TEST/', test_prefix=test_name, add_date=True)
check_result = check_ref(work_dir, test_name)
if check_result:
    print('Test passed')
else:
    print('Test failed')
    assert 0
