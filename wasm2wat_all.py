import os
import argparse

def is_wasm(file_path):
    return file_path.endswith('.wasm')

def main():
    parser = argparse.ArgumentParser(description='Run all .wasm files in a directory and its subdirectories, and log the output.')
    parser.add_argument('--path', default='/Users/hh/git/wabt/build/wasm2wat', help='Path to the root directory.')
    args = parser.parse_args()
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wasm(file_path):
                output_file = file_path.replace('.wasm', '.wat')
                command = f'{args.path} {file_path} -o {output_file}'
                os.system(command)

if __name__ == '__main__':
    main()