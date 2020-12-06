
#Libraries:

#pre-process all the information
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import re

#Create your index! - vocabularyGenerator
import csv
import json
#from preprocessor import preprocessor, download
from progress.counter import Counter
import os

from prettytable import PrettyTable
import textwrap


#define functions for pre-process the information

def download():
    nltk.download('stopwords')
    nltk.download('punkt')

def preprocessor(text: str):
    stop_words = set(stopwords.words('english')) #English stopwords
    tokens = word_tokenize(text.lower()) #tokenization
    ps = PorterStemmer() 
    result = [ps.stem(re.sub(r'[^a-zA-Z]', '', unidecode(word))) for word in tokens if word not in stop_words and word.isalpha()]

    return result



def vocabularyGenerator():
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

def invertedIndex():
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


def conjunctiveQuery():
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