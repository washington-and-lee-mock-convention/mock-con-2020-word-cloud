import logging
from datetime import date

from model import init_db, db

logging.basicConfig(level=logging.INFO)


async def setup_db():
    app = {}
    await init_db()
    app['db'] = db
    return app


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