from pathlib import Path
import os


raw_dir = r'../data/redewiedergabe/redewiedergabe_raw/fictional'
conll_dir = r'../data/redewiedergabe/redewiedergabe-conll'

if not Path(conll_dir).exists():
    os.mkdir(conll_dir)


for file in Path(raw_dir).glob('*.csv'):
    with open(file) as fin:
        with open(Path(conll_dir) / file.name, 'w') as fout:
            for line in fin:
                try:
                    token, tag1, tag2, tag3, tag4 = line[:-1].split(' ')
                except:
                    print(f'error in file', file.name)
                    next
                
                if tag1 == tag2 == tag3 == tag4 == 'O':
                    tag = 'O'
                elif tag1 == 'direct':
                    tag = tag1        
                elif tag2 == 'indirect':
                    tag = tag2        
                elif tag3 == 'reported':
                    tag = tag3        
                elif tag4 == 'freeIndirect':
                    tag = tag4
                fout.write(f'{token} {tag}\n')
        

