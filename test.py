import difflib
import sys
import os

from run import run

def check_ref(work_dir, test_name):
    #print('work_dir', work_dir)
    #print('test_name', test_name)
    res = True
    
    work_names = []
    for _root,_d_names,cur_names in os.walk(work_dir):
        work_names += cur_names
    #print(work_names)

    ref_names = []
    path_ref = 'ref/' + test_name
    for _root,_d_names,cur_names in os.walk(path_ref):
        ref_names += cur_names
    #print(ref_names)

    for ref_name in ref_names:
        found = False
        for work_name in work_names:
            if ref_name == work_name:
                found = True
                with open(path_ref+'/'+ref_name, 'r') as ref:
                    with open(work_dir+work_name, 'r') as work:
                        diff = difflib.unified_diff(
                                ref.readlines(),
                                work.readlines(),
                                fromfile=test_name+'/'+ref_name,
                                tofile=work_dir+work_name
                                )
                        for line in diff:
                             print(line)
                             res = False
        if not found:
            print('Cannot find', ref_name)
            return False
    return res

test_name = 'test1_events'
print('Run test:', test_name)
work_dir = run('ga', 'events', work_dir='TEST/', test_prefix=test_name)
check_result = check_ref(work_dir+'events/', test_name)
if check_result:
    print('Test passed')
else:
    print('Test failed')
    assert 0
