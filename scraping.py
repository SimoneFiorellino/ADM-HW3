from selenium import webdriver


def find_bookTitle():
    try:
        xpath = '//*[@id="bookTitle"]'
        bookTitle = driver.find_element_by_xpath(xpath).text
        print(bookTitle)
    except:
        print("issue in bookTitle")
        bookTitle = None

def find_bookSeries():
    try:
        xpath = '//*[@id="bookSeries"]/a'
        bookSeries = driver.find_element_by_xpath(xpath).text
        print(bookSeries)
    except:
        print("issue in bookSeries")
        bookSeries = None

def find_bookAuthors():
    try:
        xpath = '//*[@id="bookAuthors"]/span[2]/div/a/span'
        bookAuthors = driver.find_element_by_xpath(xpath).text
        print(bookAuthors)
    except:
        print("issue in bookAuthors")
        bookAuthors = None

def find_ratingValue():
    try:
        xpath = '//*[@id="bookMeta"]/span[2]'
        ratingValue = driver.find_element_by_xpath(xpath).text
        print(ratingValue)
    except:
        print("issue in ratingValue")
        ratingValue = None

def find_ratingCount():
    try:
        xpath = '//*[@id="bookMeta"]/a[2]/meta'
        ratingCount = driver.find_element_by_xpath(xpath).get_attribute('content')
        print(ratingCount)
    except:
        print("issue in ratingCount")
        ratingCount = None

def find_reviewCount():
    try:
        xpath = '//*[@id="bookMeta"]/a[3]/meta'
        reviewCount = driver.find_element_by_xpath(xpath).get_attribute('content')
        print(reviewCount)
    except:
        print("issue in reviewCount")
        reviewCount = None

def find_plot():
    try:
        xpath = '//*[@id="freeTextContainer11506544863053455196"]/b'
        plot = driver.find_element_by_xpath(xpath).getText()
        print(plot)
        # plot += '\n'
        # xpath = '//*[@id="freeText11506544863053455196"]/text()[1]'
        # plot += driver.find_element_by_xpath(xpath)
        # plot += '\n'
        # xpath += '//*[@id="freeText11506544863053455196"]/text()[1]'
        # plot = driver.find_element_by_xpath(xpath)
       
    except:
        print("issue in plot")
        plot = None

options = webdriver.ChromeOptions()
options.add_argument("--headless")

path = 'C:/Users/Simone-MSI/Desktop/dd/chromedriver.exe'
driver = webdriver.Chrome(r'E:\Universita_SAPIENZA\ADM\GitHub_HW03\chromedriver.exe', chrome_options=options)
driver.get(r'E:\Universita_SAPIENZA\ADM\GitHub_HW03\HTML_books\list_page_1\article_0')

# find_bookTitle()
# find_bookSeries()
# find_bookAuthors()
# find_ratingValue()
# find_ratingCount()

find_plot()




driver.close()