##
# Author: Alexander Caines
# Date: 10/8/2019
# Description: Given the keywords in one article, this program will query 
#   google news for other articles that mention the given keyword.
#   TL;DR, given a link, the program will find links with similar (loosely) content
# Possible Modificaitons: In order to initialize the project, rather than starting
#   with a static url, have a set of starter keywrod with which you can query google news
#   From there, do the second part of the program. 
#   TL;DR, randomly initialize the seed url
##

import html2text #converts html to text
import urllib3 #retrieves html code
import requests #for making api calls
from datetime import date #hmm

def getBuzzwords(url):
    html = getHTML(url) #html code
    text = getText(html) #text to corresponding html doc
    ftext = frequency(text.split()) #frequency of each word in the document

    #Intermediate step: clean the data. 
    ## Strip words of negligible symbols such as '*', '/', and others. 
    ## Also remove verbs and nouns

    threshold = 4
    buzzwords = keyWords(ftext, threshold) #words with frqeuencies above a certain threshold
    # print(buzzwords)
    return buzzwords
    
def getHTML(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    return r.data

def getText(html):
    html = html.decode('utf-8')
    return html2text.html2text(html)

def frequency(text):
    dictionary = []
    misc = ['had', 'has', 'was']
    articles = ['the', 'a', 'an', 'that', 'this', 'these', 'those']
    prepositions = ['of', 'with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among',
        'throughout', 'despite', 'torwards', 'upon', 'concerning', 'to', 'in', 'for', 'on', 'by', 'about',
        'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along',
        'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off',
        'above', 'near']
    for element in text:
        if((element not in prepositions) and (element not in articles) and (element not in misc)):
            dictionary.append((
                element,
                text.count(element)
            ))
    return dictionary

def keyWords(dictionary, threshold):
    ndict = []
    for item in dictionary:
        #item[0] corresponds to the word
        #item[1] corresponds to the frequency
        if item[1] >= 4:
            ndict.append(item)
    return ndict

def gnews(key, buzzwords, today):
    buzz_articles = []

    dummy_buzzword = "Trump"

    url = ('https://newsapi.org/v2/everything?'
       'q='+dummy_buzzword+'&'
       'from='+str(today)+
       'sortBy=popularity&'
       'apiKey='+str(key))
    response = requests.get(url)
    responses = response.json()

    #keys are 'status', 'totalResults', and 'articles'
    #within each article in articles, there exist eight keys:
    #'source', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content

    for i in range(0, len(responses['articles'])):
        buzz_articles.append((responses['articles'][i]['url']))
        # print(responses['articles'][i]['author']) #can vary 'author' with any of the above keys

    return buzz_articles

if __name__ == "__main__":
    url = "https://thehill.com/homenews/administration/464783-state-ordered-sondland-not-to-testify-before-house"
    buzzwords = getBuzzwords(url)
    
    api_key = "7250f963ffc04ab0bf82535a74c91358"
    today = date.today()
    articles = gnews(api_key, buzzwords, today)
    print(articles)