from preprocessor import preprocessor, download
from prettytable import PrettyTable
import textwrap
import json
import csv

download()
query = input('Query: ')
query = preprocessor(query)

with open('generated/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

with open('generated/invertedIndex.json', 'r') as json_file:
    invertedIndex = json.load(json_file)

documentList = []
for word in query:
    wordId = vocabulary[word]
    documentList.append(invertedIndex[str(wordId)])

if len(documentList) > 1:
    resultId = []
    for documentId in documentList[0]:
        common = True
        for j in range(1, len(documentList)):
            if documentId not in documentList[j]:
                common = False
                break
        if common:
            resultId.append(documentId)
else:
    resultId = documentList[0]

resultId = list(map(int, resultId))

for i in resultId:
    with open(f'TSV_books/list_page_{i // 100 + 1}/article_{i}.tsv') as tsv_file:
        tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
        row = tsv_reader.__next__()

    with open('generated/url_collected.txt') as urls:
        for j, url in enumerate(urls):
            if j == i:
                print(f"Title: {row['bookTitle']}\nUrl: {url}\nPlot:\n{row['plot']}")
                print('--------------------------------------------------')