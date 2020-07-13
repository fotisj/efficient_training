import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('data_dir', help='directory with some files to clean')
args = parser.parse_args()

for file in Path(args.data_dir).glob('*'):
    if file.is_dir():
        continue
    with open(file) as fin:
        c = 0
        for line in fin:
            try:
                lemma, tag = line[:-1].split(' ')
            except ValueError:
                print(f'ValueError: {file.name}')
                print(line)
                
            if not tag in ['O','APP','PER']:
                print(f'TagError: {file.name}')
                print(f'({c}): {line}')
            c += 1
        
    