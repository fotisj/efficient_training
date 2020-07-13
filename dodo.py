"""
    Defining workflow with doit
"""
from pathlib import Path
import os
import shutil

conll_dir = 'data/droc/droc-conll'
tei_dir = 'data/droc/droc-tei'
extra_dir = 'data/droc/droc-extra'

DOIT_CONFIG = {
 'verbosity': 2
 
}



def task_create_conll_dir():
    """make dir"""
    def create_conll_dir(targets):
        if not Path(conll_dir).exists():
            os.mkdir(conll_dir)
            
    return {
        'actions': [create_conll_dir],
        'targets': [conll_dir],
        'uptodate': [True]
    }
    

def task_convert_tei2conll():
    """tei 2 conll"""
    
    return {
        'actions': [['python', 'scripts/tei2conll.py', tei_dir, conll_dir]],
        'targets': [Path(conll_dir) / 'Zola,-Émile__Nana.tsv'],
        'uptodate': [True]
        }


def task_add_extra_files():
    """add some files not in droc"""
    def copy_files(src_dir=extra_dir, target_dir=conll_dir):
        for file in Path(src_dir).glob('*.*'):
            shutil.copy(file, target_dir)
        
    return {
        'actions': [copy_files],
        'targets': [Path(conll_dir) / 'Brand_Agenten.tsv'],
        }
            
            
def task_replace_tabs():
    def tab2blank(file_dir=conll_dir):
        for file in Path(file_dir).glob('*.tsv'):
            with open(file) as fin:
                text = fin.read()
                text = text.replace('\t',' ')
            with open(file, 'w') as fout:
                fout.write(text)
    return {
        'actions': [tab2blank],
        }
            
                