
# QUESTION_1

# Collect all the urls

# Libraries:

#get urls
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

#collecting all html pages
# from urllib.request import urlopen, Request
# from bs4 import BeautifulSoup
import re
import os

#get tsv files
# from urllib.request import urlopen, Request
# from bs4 import BeautifulSoup
# import re
# import os
import csv
from langdetect import detect
from progress.bar import IncrementalBar


#get urls
def get_urls():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    file = open("url_collected.txt", "w")  #create a file "url_collected.txt"

    for i in range(1,301):
        reg_url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={i}' #url of i-th page
        req = Request(url=reg_url, headers=headers)
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')

        for a in bs.find('table', {'class':'tableList js-dataTooltip'}).find_all('a', {'class':'bookTitle'}):
            #print(a['href'])
            file.write(f"https://www.goodreads.com{a['href']}\n") # writing the url as a line



    file.close() 


#collecting all html pages
def collect_html_pages():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    count = 0   #file index
    folder_index= 0 #folder index

    f = open("url_collected.txt", "r")
    for x in f:
        if (count % 100)==0:    #check if i need to create a new folder
            folder_index+=1
            path = f"HTML_books/list_page_{folder_index}"
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)

        req = Request(url=x, headers=headers)
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        #print(bs)
        
        #write the html page on a new file
        with open(f"{path}/article_{count}.html", "w", encoding = 'utf-8') as file:
            file.write(str(bs))
        
        count+=1


    f.close() 


#get tsv files
def get_bookTitle():
    try:
        bookTitle = next(bs.find(id='bookTitle').stripped_strings, '')
        return bookTitle
    except:
        #print("issue in bookTitle")
        return ''

def get_bookSeries():
    try:
        bookSeries = next(soup.find(id='bookSeries').stripped_strings, '')
        return bookSeries
    except:
        #print("issue in bookSeries")
        return ''

def get_bookAuthors():
    try:
        bookAuthors = ' '.join(list(bs.find(id='bookAuthors').stripped_strings)[1:])
        return bookAuthors
    except:
        return ''

def get_ratingValue():
    try:
        ratingValue = bs.find('span', {'itemprop': 'ratingValue'})
        return re.sub(r'\n\s*\n', '\n', ratingValue.text.strip())
    except:
        #print("issue in ratingValue")
        return ''

def get_ratingCount():
    try:
        ratingValue = bs.find('meta', {'itemprop': 'ratingCount'})['content']
        return ratingValue
    except:
        #print("issue in ratingCount")
        return ''

def get_reviewCount():
    try:
        reviewCount = bs.find('meta', {'itemprop': 'reviewCount'})['content']
        return reviewCount
    except:
        #print("issue in reviewCount")
        return ''

def get_plot():
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
            try:
                plot = bs.find(id='description')
                if plot != None:
                    plot = ' '.join(list(plot.stripped_strings)).replace('...more', '').replace('...less', '')
                    return plot
                else:
                    #log.write(f'[Error] #{i}: No description\n')
                    #bar.next()
                    return ''
            except:
                print("issue in plot")
                return ''
            
def get_numberofPages():
    try:
        NumberofPages = bs.find('span', {'itemprop': 'numberOfPages'})
        return re.sub(r'\s[a-zA-Z]{0,}', '', NumberofPages.text)
    except:
        print("issue in NumberofPages")
        return ''

def get_publishingDate():
    try:
        publishingDate = soup.select('#details > .row')
        if len(publishingDate) > 1:
            publishingDate = re.sub(r'(Published|\n\s*|by.*)', '', next(publishingDate[1].stripped_strings))
        else:
            publishingDate = ''
        return publishingDate
    except:
        #print("issue in publishingDate")
        return ''

def get_characters():
    try:
        characters = bs.find(text='Characters')
        if characters != None:
            characters = re.sub(r'\.\.\.\w{4}', '', ''.join(list(characters.parent.next_sibling.next_sibling.stripped_strings))).replace(',', ', ')
            return characters
        else:
            return ''
    except:
        return ''

def get_setting():
    try:
        setting = soup.find(text='Setting')
        if setting != None:
            setting = re.sub(r'…\w{4}', '', ', '.join(list(setting.parent.next_sibling.next_sibling.stripped_strings)))
        else:
            setting = ''
        return name_list
    except:
        print("issue in setting")
        return ''

def is_eng():
    try:
        if detect(get_plot()) == 'en':
            return True
        else:
            return False
    except:
        print('Issue in detect function')
        return False

def get_all_tsv():
    page_count=0    #num pages

    for folder_index in range(1,301):

        path = f"TSV/list_page_{folder_index}"
        #creating folders
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        #creating tsv 
        for _ in range(0,100):
            my_link = f'E:/Universita_SAPIENZA/ADM/GitHub_HW03/HTML_books/list_page_{folder_index}/article_{page_count}.html'
            bs = BeautifulSoup(open(my_link, encoding="utf8"), "html.parser")
            bs = bs.find('div', {'id':'metacol'})   #considering only this part of the html
            if is_eng():
                try:
                    with open(f'{path}/article_{page_count}.tsv', 'wt') as out_file:
                        tsv_writer = csv.writer(out_file, delimiter='\t')
                        tsv_writer.writerow(['bookTitle', 'bookSeries', 'bookAuthors', 'ratingValue', 'ratingCount', \
                                        'reviewCount', 'plot', 'numberofPages', 'publishingDate', 'characters', 'setting'])
                        tsv_writer.writerow([get_bookTitle(), get_bookSeries(), get_bookAuthors(), get_ratingValue(), get_ratingCount(),\
                                        get_reviewCount(), get_plot(), get_numberofPages(), get_publishingDate(), get_characters(), get_setting()])
                except:
                    print(f'issue in create {my_link}')
            page_count+=1