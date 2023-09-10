import ck.kernel as ck
import json
import subprocess
import time


def get_pro_list(dataset, start_id):
    # 执行命令
    command = 'ck list program'  # 要执行的命令
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    output = output.splitlines()
    program_list = []
    program_id = start_id

    for line in output:
        line = line.strip()
        if line.startswith(dataset):
            p = line.strip()
            print(p)
            if p == 'cbench-automotive-susan':
                dataset_uoa = 'image-pgm-0001'
                program_list.append({'dataset': dataset, 'program_name': p + '-c', 'program': p, 'id': program_id,
                                     'cmd_key': 'corners', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
                program_list.append({'dataset': dataset, 'program_name': p + '-e', 'program': p, 'id': program_id,
                                     'cmd_key': 'edges', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
                program_list.append({'dataset': dataset, 'program_name': p + '-s', 'program': p, 'id': program_id,
                                     'cmd_key': 'smoothing', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-bzip2':
                dataset_uoa = 'adpcm-0001'
                # dataset_uoa = ''
                program_list.append({'dataset': dataset, 'program_name': p + '-d', 'program': p, 'id': program_id,
                                     'cmd_key': 'decode', 'dataset_uoa': ''})
                program_id = program_id + 1
                program_list.append({'dataset': dataset, 'program_name': p + '-e', 'program': p, 'id': program_id,
                                     'cmd_key': 'encode', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-security-blowfish':
                program_id = program_id + 2
                # dataset_uoa = 'benc-0001'
                # program_list.append({'dataset': dataset, 'program_name': p + '-d', 'program': p, 'id': program_id,
                #                      'cmd_key': 'decode', 'dataset_uoa': ''})
                # program_id = program_id + 1
                # program_list.append({'dataset': dataset, 'program_name': p + '-e', 'program': p, 'id': program_id,
                #                      'cmd_key': 'encode', 'dataset_uoa': dataset_uoa})
                # program_id = program_id + 1
            elif p == 'cbench-security-rijndael':
                dataset_uoa = 'enc-0001'
                program_list.append({'dataset': dataset, 'program_name': p + '-d', 'program': p, 'id': program_id,
                                     'cmd_key': 'decode', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
                program_list.append({'dataset': dataset, 'program_name': p + '-e', 'program': p, 'id': program_id,
                                     'cmd_key': 'encode', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-consumer-jpeg-c':
                dataset_uoa = 'image-ppm-0001'
                program_list.append({'dataset': dataset, 'program_name': p, 'program': p, 'id': program_id,
                                     'cmd_key': '', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-consumer-jpeg-d':
                dataset_uoa = 'image-jpeg-0001'
                program_list.append({'dataset': dataset, 'program_name': p, 'program': p, 'id': program_id,
                                     'cmd_key': '', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-security-sha' or p == 'cbench-telecom-crc32':
                dataset_uoa = 'adpcm-0001'
                program_list.append({'dataset': dataset, 'program_name': p, 'program': p, 'id': program_id,
                                     'cmd_key': '', 'dataset_uoa': dataset_uoa})
                program_id = program_id + 1
            elif p == 'cbench-office-stringsearch2':
                # program_id = 21
                # program_list.append({'dataset': dataset, 'program_name': p, 'program': p, 'id': program_id,
                #                      'cmd_key': '', 'dataset_uoa': ''})
                program_id = program_id + 1
            elif p == 'cbench-security-pgp':
                program_id = program_id + 2
                # dataset_uoa = 'pgp-0001'
            elif p == 'cbench-consumer-mad':
                program_id = program_id + 1
                # dataset_uoa = 'audio-mp3-0001'
            else:
                program_list.append({'dataset': dataset, 'program_name': p, 'program': p, 'id': program_id,
                                     'cmd_key': '', 'dataset_uoa': ''})
                program_id = program_id + 1
    # for p in programs:
    #     r = ck.access({'action': "compile",
    #                    'module_uoa': 'program',
    #                    'data_uoa': p['program'],
    #                    'flags': '-Os',
    #                    # 'cmd_key': compiler_flags,
    #                    'out': 'con'})

    # if r['return']>0:
    #     ck.err(r)
    return program_list


if __name__ == '__main__':
    start_time = time.time()
    datasets = ['cbench', 'polybench-cpu']
    # datasets = ['cbench']
    # datasets = ['polybench-cpu']
    start_id = 1
    for d in datasets:
        program_list = get_pro_list(d, start_id)
        with open('../data/' + d + '-program_list.json', 'w') as f:
            json.dump(program_list, f)
        for p in program_list:
            print(p['id'], p['program_name'])
        start_id = program_list[-1]['id'] + 1
    end_time = time.time()
    duration = end_time - start_time

    print("程序运行时长：", duration, "秒")
