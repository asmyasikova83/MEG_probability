from run import run

def check_ref(work_dir, test_name):
    print('work_dir', work_dir)
    print('test_name', test_name)
    return  True

test_name = 'test1_events'
print('Run test:', test_name)
work_dir = run('ga', 'events', work_dir='TEST/', test_prefix=test_name)
check_result = check_ref(work_dir, test_name)
if check_result:
    print('Test passed')
else:
    print('Test failed')
    assert 0
