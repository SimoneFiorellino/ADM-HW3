from preprocessor import preprocessor, download
from conjunctiveQuery import search
import json
import csv
import heapq
import re

# download()
query = input('Query:')

query = query.lower()
pages = re.findall(r'(\d+)( |)page(s|)', query)
if len(pages) > 0:
    pages = pages[0][0]
else:
    pages = None
query = re.sub(r'\d+( |)page(s|)', '', query)
rating = re.findall(r'(\d+)( |)star(s|)', query)
if len(rating) > 0:
    rating = rating[0][0]
else:
    rating = None
query = re.sub(r'\d+( |)star(s|)', '', query)
year = re.findall(r'(^|\s)(\d{4})(\s|$)', query)
if len(year) > 0:
    year = year[0][1]
else:
    year = None
details = re.findall(r'details: (.*)$', query)
if len(details) > 0:
    details = details[0][0]
else:
    details = None
query = re.sub(r'details: (.*)$', '', query)

query = preprocessor(query)
resultId = search(query)
k = 10

with open('generated/documentNorm.json', 'r') as json_file:
    documentNorm = json.load(json_file)

with open('generated/invertedIndexTfidf.json', 'r') as json_file:
    invertedIndexTfidf = json.load(json_file)
    
with open('generated/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

plotSimilarityList = []
infoScoreList = []
pageScoreList = []
yearScoreList = []
ratingScoreList = []
for result in resultId:
    norm = documentNorm[str(result)]

    summation = 0
    for token in query:
        if token in vocabulary:
            summation += [x for x in invertedIndexTfidf[str(vocabulary[token])] if x[0] == int(result)][0][1]

    plotSimilarityList.append(summation / norm)

    with open(f'TSV_books/list_page_{result // 100 + 1}/article_{result}.tsv') as tsv_file:
        tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
        row = tsv_reader.__next__()

    if details != None:
        authorScore = len([x for x in preprocessor(details) if x in preprocessor(row['bookAuthors'])])
        charactersScore = len([x for x in preprocessor(details) if x in preprocessor(row['characters'])])
        settingScore = len([x for x in preprocessor(details) if x in preprocessor(row['setting'])])
        infoScoreList.append(authorScore + charactersScore + settingScore)
    else:
        infoScoreList.append(0)

    if pages != None and row['numberOfPages'] != '':
        pageScoreList.append(1 / (abs(int(pages) - int(row['numberOfPages'])) + 1))
    else:
        pageScoreList.append(0)

    if year != None and row['publishingDate'] != '':
        if re.search(r'\d{4}', row['publishingDate']):
            yearScoreList.append(1 / (abs(int(year) - int(re.search(r'\d{4}', row['publishingDate']).group()) + 1)))
        else:
            yearScoreList.append(0)
    else:
        yearScoreList.append(0)

    if rating != None and row['ratingValue'] != '':
        ratingScoreList.append(1 / (abs(int(rating) - float(row['ratingValue'])) + 1))
    else:
        ratingScoreList.append(0)

infoScoreList = [x / (max(infoScoreList) + 1e-6) for x in infoScoreList]
pageScoreList = [x / (max(pageScoreList) + 1e-6) for x in pageScoreList]
yearScoreList = [x / (max(yearScoreList) + 1e-6) for x in yearScoreList]
ratingScoreList = [x / (max(ratingScoreList) + 1e-6) for x in ratingScoreList]

heapResult = []
heapq.heapify(heapResult)
for i, result in enumerate(resultId):
    similarity = (plotSimilarityList[i] + infoScoreList[i] + pageScoreList[i] + yearScoreList[i] + ratingScoreList[i]) / 5
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
