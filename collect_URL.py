from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

#https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
file = open("url_collected.txt", "w") 

for i in range(1,11):
    reg_url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={i}'
    req = Request(url=reg_url, headers=headers)
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    for a in bs.find('table', {'class':'tableList js-dataTooltip'}).find_all('a', {'class':'bookTitle'}):
        #print(a['href'])
        file.write(f"https://www.goodreads.com{a['href']}\n")



file.close() 