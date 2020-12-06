# ADM-HW3

Build a search engine over the "best books ever" list of GoodReads. 

## Data collection

For this homework we have created our dataset collecting data from [Best Books Ever List](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1). We consider only 300 pages, it means a database with 30,000 books information.

After collecting all the HTML documents we extracted and saved on a tsv file these informations:

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

For this purpose the libraries used are beautifulsoup, langdetect and csv.

## Search Engine

First of all we pre-processed all the information collected for each book by

1. Removing stopwords
2. Removing all non-alphabet chars
3. Stemming
4. Tokenization

After created the dictionary and the inverted index files, we implement a simply search engine. It consider only the plot of each book.

for this phase the mainly libraries used are nltk, unidecode, json.

## Define a new score!

For the score, we first look at the query and extract useful information:
- the number of pages (if "xxx pages" is in the query)
- the number of stars in the rating (if "x stars" is in the query)
- the year (if there is 4 digit in the query)
- any details about the book (if there is a "details: ..." at the end of the query)

The 3 first informations are used to compute a distance between them and the corresponding informations of each book. For the last one, we check the intesection with the book authors, characters and settings. All this is normalized and added to the plot similarity to create a total score which is use to sort.

## Algorithmic Question

Here is a recursive method that computes the length of the maximum-length subsequence in alphabetical order with several examples.
There is also a dynamic version that takes two input strings, as seen during the lecture.
Furthermore, there is induction proof that X\[i] is correct.

## Script descriptions

1. __`q1.py`__: 
    >This script provides all the functions to create the dataset.
    >1. get_urls()
    >2. collect_html_pages()
    >3. get_all_tsv()
    
2. __`q2.py`__:
    >This script provides all the function to complete the second question.
    >1. download()
    >2. preprocessor(text: str)
 
5. __`q5.py`__: 
    >1. subsequence(st)
    >2. long_com_seq(s1 , s2)
    
    
