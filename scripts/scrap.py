from collections import defaultdict
import statistics as stat

def calc_results(target_file):
    results = defaultdict(list)
    with open(target_file) as fin:
        for line in fin:
            name, value = line[:-1].split(' = ')
            results[name].append(float(value))
    print(results)
    for key, values in results.items():
        print(f'{key}: {round(stat.mean(values), 3)} (std: {round(stat.stdev(values), 3)})')


calc_results("./results.txt")