import ck.kernel as ck
import json
import random


class CompileFailException(Exception):
    pass


class RunFailException(Exception):
    pass


def evaluate(opt_selection, program_dict, tot_opt_list, target='compile_size'):
    """
    根据全部的编译优化选项列表和编译优化选项的选择序列（01串）获得当前的编译优化选项。再根据选择的评估指标来测序列效果

    Args:
        opt_selection (list): 编译优化选项的选择序列，0为关闭，1为打开
        program_dict (dict): 测试程序的基本信息，处理过程参见'./lib/get_pro_list.py'，包括所属数据集（dataset），程序名（program_name），程序（program），序号（id），运行选项（cmd_key），运行时所选数据集（dataset_uoa）
        target (str): 评估指标，目前仅支持编译后可执行文件的大小（compile_size）和程序运行时长（run_time）
        tot_opt_list (list): 包含所有的编译优化选项，处理过程参见'./lib/get_gcc_opt.py',每个编译选项包含编译指令（compile_flag）当中第一个选项时打开，第二个时关闭，序号（flag_id），和冲突列表（conflict_list）

    Returns:
        int: 目标评估结果
    """
    # with open(opt_file) as file:
    #     tot_opt_list = json.load(file)

    compile_flag = get_opt(opt_selection, tot_opt_list)

    if target == 'compile_size':
        program = program_dict['program']
        return get_compile_size(program, compile_flag)
    elif target == 'run_time':
        program = program_dict['program']
        cmd_key = program_dict['cmd_key']
        dataset_uoa = program_dict['dataset_uoa']
        return get_run_time(program, compile_flag, cmd_key, dataset_uoa)
    else:
        print('Evaluation target that does not exist!')


def get_opt(opt_selection, tot_opt_list):
    """
    根据01串获取编译序列
    """
    compile_flag = '-Os'
    for i in range(len(opt_selection)):
        conflict_list = tot_opt_list[i]['conflict_list']
        conflict_flag = False
        for fid in conflict_list:
            if int(opt_selection[fid - 1]) == 1:
                opt_selection[i] = 0
                conflict_flag = True
        if conflict_flag:
            continue
        cur_flag = tot_opt_list[i]['compile_flag'][opt_selection[i]]
        if cur_flag != '':
            compile_flag += ' ' + cur_flag

    return compile_flag


def get_compile_size(program, compile_flag):
    """根据程序名和编译选项测试编译后可执行文件大小"""
    compile_result = ck.access({'action': "compile",
                                'module_uoa': 'program',
                                'data_uoa': program,
                                'flags': compile_flag,
                                'out': 'con'})

    if compile_result['return'] > 0:
        ck.err(compile_result)
    if compile_result['misc']['compilation_success'] == 'no':
        raise CompileFailException("编译失败！")

    return compile_result['characteristics']['obj_size']


def get_run_time(program, compile_flag, cmd_key, dataset_uoa):
    """根据程序名，编译选项和运行选项，先编译再测试运行时间"""
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
                            'out': 'con'})

    if run_result['return'] > 0:
        ck.err(run_result)
    if run_result['misc']['run_success'] == 'no':
        raise RunFailException("运行失败！")

    return run_result['characteristics']['execution_time_kernel_0']


if __name__ == '__main__':
    dataset = 'polybench-cpu'
    # dataset = 'cbench'
    with open(f'./data/{dataset}-program_list.json') as f:
        program_list = json.load(f)
    with open(f'./data/optimization_list.json') as f:
        tot_opt_list = json.load(f)
    selection = []
    for _ in range(len(tot_opt_list)):
        bit = random.choice([0, 1])
        selection.append(bit)
    for program_dict in program_list:
        evaluate(selection, program_dict, tot_opt_list, 'run_time')
        # evaluate(selection, program_dict, tot_opt_list, 'compile_size')
