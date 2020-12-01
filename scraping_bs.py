from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import os
import csv

def find_bookTitle():
    try:
        bookTitle = bs.find('h1', {'id': 'bookTitle'})
        return re.sub(r'\n\s*\n', '\n', bookTitle.text.strip())
    except:
        print("issue in bookTitle")
        return None

def find_bookSeries():
    try:
        bookSeries = bs.find('h2', {'id': 'bookSeries'})
        return re.sub(r'\n\s*\n', '\n', bookSeries.text.strip())
    except:
        print("issue in bookSeries")
        return None


def find_bookAuthors():
    try:
        bookAuthors = bs.find('a', {'class': 'authorName'})
        return re.sub(r'\n\s*\n', '\n', bookAuthors.text.strip())
    except:
        print("issue in bookAuthors")
        return None

def find_ratingValue():
    try:
        ratingValue = bs.find('span', {'itemprop': 'ratingValue'})
        return re.sub(r'\n\s*\n', '\n', ratingValue.text.strip())
    except:
        print("issue in bookAuthors")
        return None

def find_ratingCount():
    try:
        ratingValue = bs.find('meta', {'itemprop': 'ratingCount'})['content']
        return ratingValue
    except:
        print("issue in ratingValue")
        return None

def find_reviewCount():
    try:
        reviewCount = bs.find('meta', {'itemprop': 'reviewCount'})['content']
        return reviewCount
    except:
        print("issue in reviewCount")
        return None

def find_plot():
    try:
        plot = bs.find('div', {'id': 'descriptionContainer'})
        plot = plot.find_all('span')
        
        plot = plot[1].text
        return plot
    except:
        try:
            plot = plot[0].text
            return plot
        except:
            print("issue in plot")
            return None

def find_numberofPages():
    try:
        NumberofPages = bs.find('span', {'itemprop': 'numberOfPages'})
        return re.sub(r'\s[a-zA-Z]{0,}', '', NumberofPages.text)
    except:
        print("issue in NumberofPages")
        return None

def find_publishingDate():
    try:
        publishingDate = bs.find('div', {'id': 'details'}) 
        publishingDate = publishingDate.find_all('div', {'class': 'row'})
        publishingDate = (re.sub(r'\n\s*\n', '\n', publishingDate[1].text.strip()))
        publishingDate = (re.sub(r'([A-Za-z]{0,}\n[ ]{0,})', '', publishingDate))
        publishingDate = (re.sub(r'(by)([A-Za-z0-9 ()]{0,})', '', publishingDate))
        return publishingDate
    except:
        print("issue in publishingDate")
        return None

def find_characters():
    try:
        characters = bs.find_all('div', {'class': 'infoBoxRowTitle'})
        for i in characters:
            if i.text=='Characters':
                characters = i.findNext('div')
                characters = characters.find_all('a', href=re.compile(r"^/characters/"))
                name_list = ''
                for i in range(0,len(characters)-1):
                    name_list+=f'{characters[i].text}, '
                else: name_list+=f'{characters[i+1].text}'
                
                return name_list
        return 'issue'
    except:
        print("issue in characters")
        return None

def find_setting():
    try:
        characters = bs.find_all('div', {'class': 'infoBoxRowTitle'})
        for i in characters:
            if i.text=='Setting':
                setting = i.findNext('div')
                setting = setting.find_all(['a','span'])
                name_list = ''
                for i in range(0,len(setting)-1):
                    my_set = re.sub(r'\n\s*\n', '\n', setting[i].text.strip())
                    name_list+=f'{my_set}, '
                else: 
                    my_set = re.sub(r'\n\s*\n', '\n', setting[i+1].text.strip())
                    name_list+=f'{my_set}'
                return name_list
    except:
        print("issue in setting")
        return None




link = 'E:/Universita_SAPIENZA/ADM/GitHub_HW03/HTML_books/list_page_1/article_1.html'
page_count=0
for folder_index in range(1,301):

    path = f"TSV/list_page_{folder_index}"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for j in range(0,100):
        my_link = f'E:/Universita_SAPIENZA/ADM/GitHub_HW03/HTML_books/list_page_{folder_index}/article_{page_count}.html'
        bs = BeautifulSoup(open(my_link, encoding="utf8"), "html.parser")
        bs = bs.find('div', {'id':'metacol'})   #considering only the part of code inside

        try:
            with open(f'{path}/article_{page_count}.tsv', 'wt') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['bookTitle', 'bookSeries', 'bookAuthors', 'ratingValue', 'ratingCount', \
                                'reviewCount', 'plot', 'numberofPages', 'publishingDate', 'characters', 'setting'])
                tsv_writer.writerow([find_bookTitle(), find_bookSeries(), find_bookAuthors(), find_ratingValue(), find_ratingCount(),\
                                find_reviewCount(), find_plot(), find_numberofPages(), find_publishingDate(), find_characters(), find_setting()])
        except:
            print(f'issue in create {my_link}')
        page_count+=1

