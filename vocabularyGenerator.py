import csv
import json
from preprocessor import preprocessor, download
from progress.counter import Counter
import os

download()
vocabulary = dict()
bar = Counter('Progress: ')
for i in range(1, 301):
    path = f'TSV_books/list_page_{i}/'
    
    for file in os.scandir(path):
        with open(path + file.name) as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
            row = tsv_reader.__next__()['plot']

            for word in preprocessor(row):
                if word not in vocabulary.keys():
                    vocabulary[word] = len(vocabulary)
        
        bar.next()
bar.finish()

with open('generated/vocabulary.json', 'w') as json_file:
    json.dump(vocabulary, json_file)

print('File generated.')