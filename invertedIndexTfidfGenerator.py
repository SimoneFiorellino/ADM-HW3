import csv
import json
from preprocessor import preprocessor, download
from progress.counter import Counter
import os
import re
import math

download()

invertedIndexTfidf = dict()
documentNorm = dict()

with open('generated/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

with open('generated/invertedIndex.json', 'r') as json_file:
    invertedIndex = json.load(json_file)

for word in vocabulary:
    invertedIndexTfidf[vocabulary[word]] = []

n = 0
for i in range(1, 301):
    path = f'TSV_books/list_page_{i}/'
    n += len([1 for _ in os.scandir(path)])

bar = Counter('Progress: ')
for i in range(1, 301):
    path = f'TSV_books/list_page_{i}/'

    for file in os.scandir(path):
        norm = []
        with open(path + file.name) as tsv_file:
            documentId = re.sub(r'(article\_|\.tsv)', '', file.name)
            tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
            plot = tsv_reader.__next__()['plot']
            words = preprocessor(plot)

            doneWords = []
            for word in words:
                if word not in doneWords:
                    tf = len([w for w in words if w == word])
                    N = len(invertedIndex[str(vocabulary[word])])
                    idf = math.log(n/N)
                    invertedIndexTfidf[vocabulary[word]].append((int(documentId), tf * idf))
                    doneWords.append(word)

                norm.append(invertedIndexTfidf[vocabulary[word]][-1][1])

        documentNorm[documentId] = math.sqrt(sum([x**2 for x in norm]))

        bar.next()
bar.finish()


with open('generated/invertedIndexTfidf.json', 'w') as json_file:
    json.dump(invertedIndexTfidf, json_file)

with open('generated/documentNorm.json', 'w') as json_file:
    json.dump(documentNorm, json_file)

print('File generated.')