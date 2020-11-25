from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

count = 0   #options: 0, 10000, 20000
folder_index= 0
#path = f"HTML_books/list_page_{folder_index}"

f = open("url_collected.txt", "r")
for x in f:
    if (count % 100)==0:
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
    
    with open(f"{path}/article_{count}.html", "w", encoding = 'utf-8') as file:
        file.write(str(bs))
    
    count+=1


f.close() 