# ADM-HW3

Build a search engine over the "best books ever" list of GoodReads. 

## Data collection

For this homework we have created our dataset collecting data from [Best Books Ever List](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1). We consider only 300 pages, it means a database with 30,000 books information.

After collecting all the HTML documents we extract and saved on a tsv file these informations:

1. Title (to save as `bookTitle`)
2. Series (to save as `bookSeries`)
3. Author(s), the first box in the picture below (to save as `bookAuthors`)
4. Ratings, average stars (to save as `ratingValue`)
5. Number of givent ratings (to save as `ratingCount`)
6. Number of reviews (to save as `reviewCount`)
7. The entire plot (to save as `Plot`)
8. Number of pages (to save as `NumberofPages`)
9. Published (Publishing Date)
10. Characters
11. Setting

for this purpose the libraries used are beautifulsoup, langdetect and csv.

## Search Engine

First of all we pre-processed all the information collected for each book by

1. Removing stopwords
2. Removing all non-alphabet chars
3. Stemming
4. Tokenization

After create the dictionary and the inverted index json files, we implement a simply search engine. It consider only the plot of each book.

for this phase the mainly libraries used are nltk, unidecode, json, prettytable and textwrap.

## Define a new score!




## Algorithmic Question


## Script descriptions

1. __`q1.py`__: 
    >This script provides all the functions to create the dataset.
    >1. get_urls()
    >2. collect_html_pages()
    >3. get_all_tsv()
    >4. all the functions for each information saved on the tsv.
    
1. __`q2.py`__:
    >This script provides all the function to complete the second question.
    >1. download()
    >2. preprocessor(text: str)
    >3. vocabularyGenerator()
    >4. invertedIndex()
    >5. conjunctiveQuery()
    
    