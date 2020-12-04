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
    # Empty files IDs: [9, 271,317,392,700,765,1082,1247,1386,1574,1964,2078,2079,2108,2170,2222,2287,2297,2326,2336,3035,3512,3531,3679,3694,3798,3825,4100,4124,4132,4414,4737,4752,4960,5329,5385,5402,5537,5689,5763,5800,6313,6377,6496,6555,6772,7012,7164,7194,7238,7725,8106,8109,8306,8748,9001,9014,9015,9304,9322,9475,10068,10313,10408,10536,10916,11020,11057,11700,11843,12375,12479,12506,12510,12624,12771,12864,12912,14122,14407,15114,15261,15354,15970,16413,16505,16587,16624,16988,17302,17410,17631,17740,17812,18878,19291,19413,19660,19908,19976,21802,21845,22386,22787,23162,24091,24974,26159,26281,26680,27051,27091,27722,27987,28080,29669,29974,29980]
    if count not in [12771,12864,12912,14122,14407,15114,15261,15354,15970,16413,16505,16587,16624,16988,17302,17410,17631,17740,17812,18878,19291,19413,19660,19908,19976,21802,21845,22386,22787,23162,24091,24974,26159,26281,26680,27051,27091,27722,27987,28080,29669,29974,29980]:
        count += 1
        continue

    # if (count % 100)==0:
    #     folder_index+=1
    #     path = f"HTML_books/list_page_{folder_index}"
    #     try:
    #         os.mkdir(path)
    #     except OSError:
    #         print ("Creation of the directory %s failed" % path)
    #     else:
    #         print ("Successfully created the directory %s " % path)

    req = Request(url=x, headers=headers)
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    #print(bs)
    
    with open(f"HTML_books/list_page_{count // 100 + 1}/article_{count}.html", "w", encoding = 'utf-8') as file:
        file.write(str(bs))
    
    count+=1
    print(f"HTML_books/list_page_{count // 100 + 1}/article_{count}.html")
f.close() 