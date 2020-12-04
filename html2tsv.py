from bs4 import BeautifulSoup
from langdetect import detect
import re
import csv
from progress.bar import IncrementalBar
import os

# for i in range(1,301):
#   try:
#     os.mkdir(f'TSV_books/list_page_{i}')
#   except:
#     print(f'Error when creating folder #{i}')

with open('info.log', 'a') as log:
  numberOfBook = 300 * 100
  bar = IncrementalBar('Progress', max = numberOfBook)

  for i in [11700,11843,12375,12479,12506,12510,12624,12771,12864,12912,14122,14407,15114,15261,15354,15970,16413,16505,16587,16624,16988,17302,17410,17631,17740,17812,18878,19291,19413,19660,19908,19976,21802,21845,22386,22787,23162,24091,24974,26159,26281,26680,27051,27091,27722,27987,28080,29669,29974,29980]:

    soup = BeautifulSoup(open(f'HTML_books/list_page_{i // 100 + 1}/article_{i}.html'), features='html.parser')
    soup = soup.find(id='metacol')

    if soup == None:
      log.write(f'[Error] #{i}: Empty file ?\n')
      bar.next()
      continue

    # Get plot
    plot = soup.find(id='description')
    if plot != None:
      plot = ' '.join(list(plot.stripped_strings)).replace('...more', '').replace('...less', '')
    else:
      log.write(f'[Error] #{i}: No description\n')
      bar.next()
      continue

    # Check if the plot is in english
    try:
      if detect(plot) != 'en':
        log.write(f'[Info] #{i}: Skipped\n')
        bar.next()
        continue
    except:
      log.write(f'[Error] #{i}: Error with langdetect\n')
      continue

    # Get bookTitle
    bookTitle = next(soup.find(id='bookTitle').stripped_strings, '')

    # Get bookSeries
    bookSeries = next(soup.find(id='bookSeries').stripped_strings, '')

    # Get bookAuthors
    bookAuthors = ' '.join(list(soup.find(id='bookAuthors').stripped_strings)[1:])

    # Get ratingValue
    ratingValue = next(soup.find(itemprop='ratingValue').stripped_strings, '')

    # Get ratingCount and reviewCount
    ratingCount = soup.find(itemprop='ratingCount').attrs.get('content')
    reviewCount = soup.find(itemprop='reviewCount').attrs.get('content')

    # Get numberOfPages
    numberOfPages = soup.find(itemprop='numberOfPages')
    if numberOfPages != None:
      numberOfPages = next(soup.find(itemprop='numberOfPages').stripped_strings, '').replace(' pages', '')
    else:
      numberOfPages = ''

    # Get publishingDate
    publishingDate = soup.select('#details > .row')
    if len(publishingDate) > 1:
      publishingDate = re.sub(r'(Published|\n\s*|by.*)', '', next(publishingDate[1].stripped_strings))
    else:
      publishingDate = ''

    # Get characters
    characters = soup.find(text='Characters')
    if characters != None:
      characters = re.sub(r'\.\.\.\w{4}', '', ''.join(list(characters.parent.next_sibling.next_sibling.stripped_strings))).replace(',', ', ')
    else:
      characters = ''

    # Get setting
    setting = soup.find(text='Setting')
    if setting != None:
      setting = re.sub(r'…\w{4}', '', ', '.join(list(setting.parent.next_sibling.next_sibling.stripped_strings)))
    else:
      setting = ''

    # Write TSV file
    with open(f'TSV_books/list_page_{i // 100 + 1}/article_{i}.tsv', 'w') as tsv:
      tsv_writer = csv.writer(tsv, delimiter='\t')
      tsv_writer.writerow(['bookTitle', 'bookSeries', 'plot', 'bookAuthors', 'ratingValue', 'ratingCount', 'reviewCount', 'numberOfPages', 'publishingDate', 'characters', 'setting'])
      tsv_writer.writerow([bookTitle, bookSeries, plot, bookAuthors, ratingValue, ratingCount, reviewCount, numberOfPages, publishingDate, characters, setting])
    
    log.write(f'[Info] #{i}: Success\n')

    bar.next()
  
  bar.finish()