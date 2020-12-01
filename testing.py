from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import os

def find_bookTitle():
    try:
        bookTitle = bs.find('h1', {'id': 'bookTitle'})
        print(re.sub(r'\n\s*\n', '\n', bookTitle.text.strip()))
    except:
        print("issue in bookTitle")
        bookTitle = None

def find_bookSeries():
    try:
        bookSeries = bs.find('h2', {'id': 'bookSeries'})
        print(re.sub(r'\n\s*\n', '\n', bookSeries.text.strip()))
    except:
        print("issue in bookSeries")
        bookSeries = None


def find_bookAuthors():
    try:
        bookAuthors = bs.find('a', {'class': 'authorName'})
        print(re.sub(r'\n\s*\n', '\n', bookAuthors.text.strip()))
    except:
        print("issue in bookAuthors")
        bookAuthors = None

def find_ratingValue():
    try:
        ratingValue = bs.find('span', {'itemprop': 'ratingValue'})
        print(re.sub(r'\n\s*\n', '\n', ratingValue.text.strip()))
    except:
        print("issue in bookAuthors")
        ratingValue = None

def find_ratingCount():
    try:
        ratingValue = bs.find('meta', {'itemprop': 'ratingCount'})['content']
        print(ratingValue)
    except:
        print("issue in ratingValue")
        ratingValue = None

def find_reviewCount():
    try:
        reviewCount = bs.find('meta', {'itemprop': 'reviewCount'})['content']
        print(reviewCount)
    except:
        print("issue in reviewCount")
        reviewCount = None

def find_plot():
    try:
        plot = bs.find('div', {'id': 'descriptionContainer'})
        plot = plot.find_all('span')
        
        plot = plot[1].text
        print(plot)
    except:
        try:
            plot = plot[0].text
            print(plot)
        except:
            print("issue in plot")
            plot = None

def find_numberofPages():
    try:
        NumberofPages = bs.find('span', {'itemprop': 'numberOfPages'})
        print(re.sub(r'\s[a-zA-Z]{0,}', '', NumberofPages.text))
    except:
        print("issue in NumberofPages")
        NumberofPages = None

def find_publishingDate():
    try:
        publishingDate = bs.find('div', {'id': 'details'}) 
        publishingDate = publishingDate.find_all('div', {'class': 'row'})
        publishingDate = (re.sub(r'\n\s*\n', '\n', publishingDate[1].text.strip()))
        print(publishingDate)
    except:
        print("issue in publishingDate")
        publishingDate = None

def find_characters():
    try:
        characters = bs.find_all('div', {'class': 'clearFloats'}) 
        characters = characters[4].find('div', {'class': 'infoBoxRowItem'})
        characters = characters.find_all("a", href=re.compile(r"^/characters/"))
        name_list = ''
        for i in range(0,len(characters)-1):
            name_list+=f'{characters[i].text}, '
        else: name_list+=f'{characters[i+1].text}'
        print(name_list)
    except:
        print("issue in characters")
        characters = None

def find_setting():
    try:
        setting = bs.find_all('div', {'class': 'infoBoxRowItem'}) 
        setting = setting[5].find_all(['a','span'])
        name_list = ''
        for i in range(0,len(setting)-1):
            my_set = re.sub(r'\n\s*\n', '\n', setting[i].text.strip())
            name_list+=f'{my_set}, '
        else: 
            my_set = re.sub(r'\n\s*\n', '\n', setting[i+1].text.strip())
            name_list+=f'{my_set}'
        print(name_list)
    except:
        print("issue in setting")
        setting = None

bs = BeautifulSoup(open("E:/Universita_SAPIENZA/ADM/GitHub_HW03/HTML_books/list_page_1/article_0.html", encoding="utf8"), "html.parser")
bs = bs.find('div', {'id':'metacol'})   #considering only the part of code inside

find_bookTitle()
find_bookSeries()
find_bookAuthors()
find_ratingValue()
find_ratingCount()
find_reviewCount()
find_plot()
find_numberofPages()
find_publishingDate()
find_characters()
find_setting()