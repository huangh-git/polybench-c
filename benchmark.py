import os
import sys
import subprocess
import argparse
import re
import math

def is_wasm(file_path, suf):
    return file_path.endswith(suf)


def execute_and_log(executable, log_file, wasmtime_path, out_arr, run_option = ""):
    # print(f'{executable}, {log_file}, {wasmtime_path}')
    with open(log_file, 'a') as log:
        # 运行 wasm 文件使用 
        # if exe_type != 0:
        result = subprocess.run(['./utilities/time_benchmark.sh', executable,  wasmtime_path, run_option], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # else:
        #     result = subprocess.run(['./utilities/time_benchmark_native.sh', executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.write(f'Running {executable}...\n')
        log.write(result.stdout + ' ' + run_option + '\n')
        log.write(result.stderr + '\n')
        match = re.search(r'\[INFO\] Normalized time: (\d+\.\d+)', result.stdout)
        if match:
            normalized_time = float(match.group(1))
            out_arr.append(normalized_time)
        else:
            print('No match found in stdout.')
            exit(1)

def main():
    parser = argparse.ArgumentParser(description='Run all .wasm files in a directory and its subdirectories, and log the output.')
    parser.add_argument('--log', default='output.log', help='Path to the log file.')
    parser.add_argument('--wasmtime', default='/Users/hh/git/wasmtime/target/debug/wasmtime', help='Path to the wasmtime')
    parser.add_argument('--suffix', default='.wasm', help='Path to the root directory.')
    args = parser.parse_args()

    log_file = args.log
    wasmtime_path = args.wasmtime
    suf = args.suffix

    # Clear or create the log file
    open(log_file, 'w').close()
    testfiles = []
    nativeT = []
    rawWasmT = []
    storeCheckT = []
    memsWasmT = []
    upperCheckT = []

    # run files
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wasm(file_path, suf):
                execute_and_log(file_path, log_file, wasmtime_path, memsWasmT) #mems wasm
                execute_and_log(file_path, log_file, wasmtime_path, storeCheckT, "--store-check-only") #mems wasm store check only
                execute_and_log(file_path, log_file, wasmtime_path, upperCheckT, "--upper-check-only")
                execute_and_log(file_path.replace(suf, ".raw-wasm"), log_file, wasmtime_path, rawWasmT) #raw
                execute_and_log(file_path.replace(suf, ".native"), log_file, "", nativeT) #native
                testfiles.append(file_path.replace(suf, ""))

    print(f'Run finished. Output logged to {log_file}')
    length = len(testfiles)
    # raw_sum_ration = 0.0
    # mems_sum_ration = 0.0
    raw_acc_overheads = 1.0
    mems_acc_overheads = 1.0
    store_acc_overheads = 1.0
    upper_acc_overheads = 1.0
    with open("result.log", 'w') as log:
        log.write(f'{" ":<55} {"rawWasmRatio":<15} {"storeOnlyRatio":<15} {"upperOnlyRatio":<15} {"memsWasmRatio":<15}\n')
        for i in range(length):
            rawWasmRatio = rawWasmT[i]/nativeT[i]
            memsWasmRatio = memsWasmT[i]/nativeT[i]
            storeOnlyRatio = storeCheckT[i]/nativeT[i]
            upperOnlyRatio = upperCheckT[i]/nativeT[i]
            print(f'{testfiles[i]:<55} : nativeT:{nativeT[i]:<5.8f}s')
            print(f'\trawWasmT:{rawWasmT[i]:<5.8f}s, upperOnlyCheckT:{upperCheckT[i]:<5.8f}s, storeOnlyCheckT:{storeCheckT[i]:<5.8f}s, memsWasmT:{memsWasmT[i]:<5.8f}s,', end='')
            print(f'rawWasmRatio:{rawWasmRatio:<5.8f}, upperOnlyCheckRatio:{upperOnlyRatio:<5.8f}s, storeOnlyCheckRatio:{storeOnlyRatio:<5.8f}s, memsWasmRatio:{memsWasmRatio:<5.8f}')
            # print(f'\trawWasmT:{rawWasmT[i]:<5.8f}s, storeOnlyCheckT:{storeCheckT[i]:<5.8f}s, memsWasmT:{memsWasmT[i]:<5.8f}s,', end='')
            # print(f'rawWasmRatio:{rawWasmRatio:<5.8f}, storeOnlyCheckRatio:{storeOnlyRatio:<5.8f}s, memsWasmRatio:{memsWasmRatio:<5.8f}')
            # log.write(f'{testfiles[i]:<55},{rawWasmRatio:<10.5f},{storeOnlyRatio:<10.5},{memsWasmRatio:<10.5f}\n')
            log.write(f'{testfiles[i]:<55},{rawWasmRatio:<10.5f},{storeOnlyRatio:<10.5},{upperOnlyRatio:<10.5},{memsWasmRatio:<10.5f}\n')
            raw_acc_overheads *= rawWasmRatio
            upper_acc_overheads *= upperOnlyRatio
            store_acc_overheads *= storeOnlyRatio
            mems_acc_overheads *= memsWasmRatio
            # raw_sum_ration += rawWasmRatio
            # mems_sum_ration += memsWasmRatio
        # print("mean average overhead:", sum_overheads/length)
        # geomean
        raw_geomean = math.pow(raw_acc_overheads, 1/length)
        upper_geomean = math.pow(upper_acc_overheads, 1/length)
        store_geomean = math.pow(store_acc_overheads, 1/length)
        mems_geomean = math.pow(mems_acc_overheads, 1/length)

        print("geometric average overhead for raw wasm:", raw_geomean)
        print("geometric average overhead for upper check only:", upper_geomean)
        print("geometric average overhead for store check only:", store_geomean)
        print("geometric average overhead for mems wasm:", mems_geomean)
        print("overhead for upper check only:", (upper_geomean - raw_geomean)/raw_geomean)
        print("overhead for store check only:", (store_geomean - raw_geomean)/raw_geomean)
        print("overhead for mems wasm:", (mems_geomean - raw_geomean)/raw_geomean)
        # print("mean average overhead for raw wasm:", raw_sum_ration/length)
        # print("mean average overhead for mems wasm:", mems_sum_ration/length)

        # log.write(f"geometric average overhead for raw wasm: {math.pow(raw_acc_overheads, 1/length)}\n")
        # log.write(f"geometric average overhead for mems wasm: {math.pow(mems_acc_overheads, 1/length)}\n")

if __name__ == '__main__':
    main()
