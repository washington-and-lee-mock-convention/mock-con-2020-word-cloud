import logging
from datetime import date

from model import init_db, db

logging.basicConfig(level=logging.INFO)


async def setup_db():
    app = {}
    await init_db()
    app['db'] = db
    return app


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


def word_seed():
    return [
        'biden', 'warren', 'sanders', 'DNC', 'harris', 'iowa', 'nevada', 'new+hampshire', 'south+carolina',
        'delegates', 'campaign+infrastructure', 'paid+staff', 'volunteers', 'path+to+victory'
    ]


def create_newsapi_url(words, key):
    url = f'https://newsapi.org/v2/everything?q={"+".join(words)}&from={str(date.today())}sortBy=popularity&apiKey={str(key)}'
    logging.info(f'Querying NewsAPI with: {url}')
    return url


def create_google_news_url(words):
    url = f'https://news.google.com/rss/search?q={"+".join(words)}'
    logging.info(f'Querying Google News with: {url}')
    return url