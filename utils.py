import logging
from datetime import date

logging.basicConfig(level=logging.INFO)


def define_forbidden_words():
    dictionary = {}
    misc = ['had', 'has', 'was', 'is', 'are', 'have']
    articles = ['the', 'a', 'an', 'that', 'this', 'these', 'those']
    prepositions = ['of', 'with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among',
        'throughout', 'despite', 'torwards', 'upon', 'concerning', 'to', 'in', 'for', 'on', 'by', 'about',
        'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along',
        'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off',
        'above', 'near']
    conjunctions = ['for', 'and', 'so', 'but', 'not', 'yet', 'nor', 'or']
    pronouns = [
        'i', 'me', 'we', 'us', 'our', 'you', 'your', 'he', 'his', 'him',
        'she', 'her', 'it', 'they', 'their'
    ]

    forbidden_words = []
    for wset in [misc, articles, prepositions, conjunctions, pronouns]:
        forbidden_words.extend(wset)
    return forbidden_words


def create_newsapi_url(words, key):
    url = f'https://newsapi.org/v2/everything?q={"+".join(words)}&from={str(date.today())}sortBy=popularity&apiKey={str(key)}'
    logging.info(f'Querying NewsAPI with: {url}')
    return url