import json


def get_gcc_optimizations(compiler_dict):
    optimization_list = []
    flag_id = 1
    for i in compiler_dict['all_compiler_flags_desc']:
        if i.startswith("##bool"):
            choice = compiler_dict['all_compiler_flags_desc'][i]['choice']
            if len(choice) == 1:
                optimization_list.append({'compile_flag': ['', choice[0]], 'flag_id': flag_id, 'conflict_list':[]})
                flag_id += 1
            elif len(choice) == 2 and choice[1].startswith("-fno"):
                if choice[0] == '-fsection-anchors':
                    continue
                if choice[0] == '-fdelayed-branch':
                    continue
                if choice[0] == '-fassociative-math':
                    continue
                if choice[0] == '-funit-at-a-time':
                    continue
                if choice[0] == '-fwhole-program':
                    continue
                if choice[0] == '-fprefetch-loop-arrays':
                    continue
                optimization_list.append({'compile_flag': [choice[0], choice[1]], 'flag_id': flag_id, 'conflict_list':[]})
                flag_id += 1
            else:
                conflict_list = []
                for c in choice:
                    optimization_list.append({'compile_flag': ['', c], 'flag_id': flag_id, 'conflict_list': conflict_list.copy()})
                    conflict_list.append(flag_id)
                    flag_id += 1

    return optimization_list


if __name__ == '__main__':
    with open('../data/compiler_desc.json') as f:
        compiler_dict = json.load(f)

    optimization_list = get_gcc_optimizations(compiler_dict)
    print(len(optimization_list))
    if optimization_list:
        print("GCC Optimizations:")
        for opt in optimization_list:
            print(opt)
    with open('../data/optimization_list.json', 'w') as f:
        json.dump(optimization_list, f)
