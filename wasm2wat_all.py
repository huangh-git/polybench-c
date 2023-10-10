import os

def is_wasm(file_path):
    return file_path.endswith('.wasm')

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wasm(file_path):
                output_file = file_path.replace('.wasm', '.wat')
                command = f'/Users/hh/git/wabt/build/wasm2wat {file_path} -o {output_file}'
                os.system(command)

if __name__ == '__main__':
    main()