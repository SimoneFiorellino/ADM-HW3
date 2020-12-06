from preprocessor import preprocessor, download
from conjunctiveQuery import search
import json
import csv
import heapq

download()
query = input('Query: ')
query = preprocessor(query)
resultId = search(query)
k = 10

with open('generated/documentNorm.json', 'r') as json_file:
    documentNorm = json.load(json_file)

with open('generated/invertedIndexTfidf.json', 'r') as json_file:
    invertedIndexTfidf = json.load(json_file)
    
with open('generated/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

heapResult = []
heapq.heapify(heapResult)
for result in resultId:
    norm = documentNorm[str(result)]

    summation = 0
    for token in query:
        if token in vocabulary:
            summation += [x for x in invertedIndexTfidf[str(vocabulary[token])] if x[0] == int(result)][0][1]

    similarity = summation / norm

    heapq.heappush(heapResult, (similarity, result))

for i in heapq.nlargest(k, heapResult):
    with open(f'TSV_books/list_page_{i[1] // 100 + 1}/article_{i[1]}.tsv') as tsv_file:
        tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
        row = tsv_reader.__next__()

    with open('generated/url_collected.txt') as urls:
        for j, url in enumerate(urls):
            if j == i[1]:
                print(f"Title: {row['bookTitle']}\nUrl: {url}\nSimilarity: {i[0]}\nPlot:\n{row['plot']}")
                print('--------------------------------------------------')
