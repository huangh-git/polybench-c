import os
import re

def replace_main_in_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    new_content = re.sub(r'int main\(int argc, char\*\* argv\)', 'int main()', content)

    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.c'):
                file_path = os.path.join(root, file)
                replace_main_in_file(file_path)

if __name__ == '__main__':
    main()

