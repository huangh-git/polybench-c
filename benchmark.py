import os
import subprocess
import argparse


SUFFIX = ".wasm"

def is_wasm(file_path):
    return file_path.endswith(SUFFIX)

def execute_and_log(executable, log_file):
    with open(log_file, 'a') as log:
        # 运行 wasm 文件使用 wasmer
        result = subprocess.run(['./utilities/time_benchmark.sh', executable,  '/Users/hh/git/wasmtime/target/debug/wasmtime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.write(f'Running {executable}...\n')
        log.write(result.stdout + '\n')
        log.write(result.stderr + '\n')

def main():
    parser = argparse.ArgumentParser(description='Run all .wasm files in a directory and its subdirectories, and log the output.')
    parser.add_argument('--log', default='output.log', help='Path to the log file.')
    parser.add_argument('--suffix', default='.wasm', help='Path to the root directory.')
    args = parser.parse_args()

    log_file = args.log
    SUFFIX = args.suffix

    # Clear or create the log file
    open(log_file, 'w').close()

    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wasm(file_path):
                execute_and_log(file_path, log_file)
                execute_and_log(file_path.replace(".wasm", ".raw-wasm"), log_file)

    print(f'Script finished. Output logged to {log_file}')

if __name__ == '__main__':
    main()
