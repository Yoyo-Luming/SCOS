import ck.kernel as ck


class CompileFailException(Exception):
    pass


class RunFailException(Exception):
    pass


program = 'cbench-telecom-crc32'
# cbench-telecom-crc32
# program = 'cbench-automotive-qsort1'

compile_flag = '-Os'
cmd_key = ''
# cmd_key = 'encode'
dataset_uoa = ''
# dataset_uoa = 'data'
dataset_file = ''
# dataset_file = 'data.s.txt'

compile_result = ck.access({'action': "compile",
                            'module_uoa': 'program',
                            'data_uoa': program,
                            'flags': compile_flag,
                            'out': 'con'})

if compile_result['return'] > 0:
    ck.err(compile_result)

if compile_result['misc']['compilation_success'] == 'no':
    raise CompileFailException("编译失败！")

run_result = ck.access({'action': "run",
                        'module_uoa': 'program',
                        'data_uoa': program,
                        'cmd_key': cmd_key,
                        'dataset_uoa': dataset_uoa,
                        'dataset_file': dataset_file,
                        'out': 'con'})

if run_result['return'] > 0:
    ck.err(run_result)

if run_result['misc']['run_success'] == 'no':
    raise RunFailException("运行失败！")
