"""
crossvalidates training the NER task using the token-classification script from huggingface
"""

import argparse, json, random, os, shutil, time
from collections import defaultdict
from pathlib import Path
import sys
from transformers import AutoTokenizer
import statistics as stat

def prepare_all_data(data_dir, n_folds):
    filelist = list(Path(data_dir).glob('*'))
    return datapoints2folds(n_folds, filelist)
    

def clear_dir(directory):
    shutil.rmtree(directory)    


def prepare_data(data_dir, fold, folds):
    if Path(data_dir).exists():
        clear_dir(data_dir)
    os.mkdir(data_dir)
    with open(Path(data_dir) / 'test.tmp', 'a') as fout1:
        with open(Path(data_dir) / 'dev.tmp', 'a') as fout2:
            for file in fold:
                with open(file) as fin:
                    text = fin.read()
                    fout1.write(text)
                    fout2.write(text)

    with open(Path(data_dir) / 'train.tmp', 'a') as fout:
        for train_fold in folds:
            if train_fold != fold:
                for file in train_fold:
                    with open(file) as fin:
                        text = fin.read()
                        fout.write(text)


def fine_tuning(script_file, config_file):
    os.system(f'python {script_file} {config_file}')


def remove_trained_model(model_dir):
    clear_dir(model_dir)


def save_test_results(results_file, target_file):
    print('\n\n---------------------------------------------------------------')
    print(f'saving {results_file} in 3 secs')
    time.sleep(3)
    shutil.copy(results_file, r'D:\mydata\Dropbox\uni\AUFSATZ\2020 Computational Humanities - Efficient historical modeling')    
    with open(target_file, 'a') as fout:
        with open(Path(results_file)) as fin:
            fout.write(fin.read())
    print('\n---------------------------------------------------------------')
    print(f'results saved in {results_file} continuing in 3 secs')
    time.sleep(3)
        

def calc_results(target_file):
    results = defaultdict(list)
    with open(target_file) as fin:
        for line in fin:
            name, value = line[:-1].split(' = ')
            results[name].append(float(value))
    print(results)
    for key, values in results.items():
        print(f'{key}: {round(stat.mean(values), 3)} (std: {round(stat.stdev(values), 3)})')

        
def preprocess_file(dataset, output, model_name_or_path, max_len):
    """Adapted from the preprocess script in huggingface / examples / token-classification from 
    """
    subword_len_counter = 0

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    max_len -= tokenizer.num_special_tokens_to_add()

    with open(output, 'w') as fout:
        with open(dataset, "rt") as f_p:
            for line in f_p:
                line = line.rstrip()

                if not line:
                    fout.write(f'{line}\n')
                    subword_len_counter = 0
                    continue

                token = line.split()[0]

                current_subwords_len = len(tokenizer.tokenize(token))

                # Token contains strange control characters like \x96 or \x95
                # Just filter out the complete line
                if current_subwords_len == 0:
                    continue

                if (subword_len_counter + current_subwords_len) > max_len:
                    fout.write(f'\n')
                    fout.write(f'{line}\n')
                    subword_len_counter = current_subwords_len
                    continue

                subword_len_counter += current_subwords_len
                fout.write(f'{line}\n')
    

def preprocessing(data_dir, model_name):
    files = ['train.tmp', 'dev.tmp', 'test.tmp']
    #model_name = 'bert-base-german-dbmdz-cased'
    length = 128
    target_dir = r'D:\mydata\Dropbox\uni\AUFSATZ\2020 Computational Humanities - Efficient historical modeling\tmp\run_0'

    for file in files:
        in_file = Path(data_dir) / file
        preprocess_file(in_file, in_file.with_suffix('.txt'), model_name, length)
        shutil.copy(in_file.with_suffix('.txt'), target_dir)


def datapoints2folds(n_folds, datapoints):
    random.seed(42)
    random.shuffle(datapoints)
    
    folds = [[] for _ in range(n_folds)]
    i = 0
    for x in datapoints:
        folds[i].append(x)
        i += 1
        if i == n_folds: i = 0
    return folds
    

def cross_validate(n_folds, data_src_dir, data_dir, pretrained_model, finetuned_model, 
                   script_file, config_file, result_file, all_results_file):
    folds = prepare_all_data(data_src_dir, int(n_folds))
    c = 1
    for fold in folds:
        print(f'\n\n\nCrossvalidation fold ({c}/{n_folds})\n\n')
        prepare_data(data_dir, fold, folds)
        preprocessing(data_dir, pretrained_model)
        fine_tuning(script_file, config_file)
        save_test_results(result_file, all_results_file)
        remove_trained_model(finetuned_model)
        c += 1
    calc_results(all_results_file)
    

def read_config(file):
    """
    TODO add sanity check
    """
    with open(file) as fin:
        return json.loads(fin.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='Name of the json file which contains the configuration information')
    args = parser.parse_args()
    cfg = read_config(args.config_file)
    
    cross_validate(cfg['n_folds'], cfg['data_src_dir'], cfg['data_dir'], 
                   cfg['pretrained_model'], cfg['finetuned_model'], cfg['script_file'], 
                   cfg['config_file'], cfg['result_file'], cfg['all_results_file'])
    

if __name__ == "__main__":
    main()

