import os
import subprocess
import argparse
import re
import math

def is_wasm(file_path):
    return file_path.endswith('.wasm')

testfiles = []
overheads = []
tmp_time = 0.0

def execute_and_log(executable, log_file):
    with open(log_file, 'a') as log:
        # 运行 wasm 文件使用 wasmer
        result = subprocess.run(['./utilities/time_benchmark.sh', executable,  '/Users/hh/git/wasmtime/target/debug/wasmtime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.write(f'Running {executable}...\n')
        log.write(result.stdout + '\n')
        log.write(result.stderr + '\n')
        match = re.search(r'\[INFO\] Normalized time: (\d+\.\d+)', result.stdout)
        if match:
            normalized_time = float(match.group(1))
            if is_wasm(executable):
                global tmp_time
                tmp_time = normalized_time
            else:
                oh = (tmp_time - normalized_time)/normalized_time
                if oh < 0:
                    oh = 0.00001
                overheads.append(oh)
        else:
            print('No match found in stdout.')
            exit(1)

def main():
    parser = argparse.ArgumentParser(description='Run all .wasm files in a directory and its subdirectories, and log the output.')
    parser.add_argument('--log', default='output.log', help='Path to the log file.')
    # parser.add_argument('--suffix', default='.wasm', help='Path to the root directory.')
    args = parser.parse_args()

    log_file = args.log

    # Clear or create the log file
    open(log_file, 'w').close()

    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wasm(file_path):
                execute_and_log(file_path, log_file)
                execute_and_log(file_path.replace(".wasm", ".raw-wasm"), log_file)
                testfiles.append(file_path[:-5])

    print(f'Script finished. Output logged to {log_file}')
    length = len(testfiles)
    sum_overheads = 0.0
    acc_overheads = 1.0
    for i in range(length):
        print(f'{testfiles[i]:<55}, {overheads[i]:<10.5f}')
        sum_overheads += overheads[i]
        acc_overheads *= overheads[i]
    print("mean average overhead:", sum_overheads/length)
    print("geometric average overhead:", math.pow(acc_overheads, 1/length))

if __name__ == '__main__':
    main()
