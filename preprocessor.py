import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import re

def download():
    nltk.download('stopwords')
    nltk.download('punkt')
    
    return

def preprocessor(text: str):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    ps = PorterStemmer()
    
    result = [ps.stem(re.sub(r'[^a-zA-Z]', '', unidecode(word))) for word in tokens if word not in stop_words and word.isalpha()]

    return result