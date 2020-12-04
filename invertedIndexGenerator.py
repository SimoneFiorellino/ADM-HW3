import csv
import json
from preprocessor import preprocessor, download
from progress.counter import Counter
import os
import re

download()

invertedIndex = dict()

with open('generated/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

for word in vocabulary:
    invertedIndex[vocabulary[word]] = []

bar = Counter('Progress: ')
for i in range(1, 301):
    path = f'TSV_books/list_page_{i}/'
    
    for file in os.scandir(path):
        with open(path + file.name) as tsv_file:
            documentId = re.sub(r'(article\_|\.tsv)', '', file.name)
            tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
            row = tsv_reader.__next__()['plot']

            for word in preprocessor(row):
                if documentId not in invertedIndex[vocabulary[word]]:
                    invertedIndex[vocabulary[word]].append(documentId)
        
        bar.next()
bar.finish()


with open('generated/invertedIndex.json', 'w') as json_file:
    json.dump(invertedIndex, json_file)

print('File generated.')