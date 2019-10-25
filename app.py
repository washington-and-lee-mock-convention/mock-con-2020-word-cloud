import os
import asyncio
import connexion
import logging
from connexion.resolver import RestyResolver
from newsapi_courier import NewsAPICourier
from cloud_generator import WordCloudGenerator
from googlenews_courier import GoogleNewsCourier
from model import init_db, db
from utils import define_forbidden_words, create_newsapi_url, create_google_news_url

API_PORT = os.environ.get('API_PORT', 8080)
FORBIDDEN_WORDS = os.environ.get('FORBIDDEN_WORDS', define_forbidden_words())
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '7250f963ffc04ab0bf82535a74c91358')
THRESHOLD = os.environ.get('THRESHOLD', 0)

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

query_newsapi = NewsAPICourier(loop, WordCloudGenerator(FORBIDDEN_WORDS, THRESHOLD))
query_google = GoogleNewsCourier(loop)


async def setup_recurring_newsapi_scrape():
    while True:
        logging.info('Querying News API...')
        # Will need to incorporate a service to create word combinations
        placeholder = ['Trump']
        await query_newsapi(create_newsapi_url(placeholder, NEWSAPI_KEY))
        await asyncio.sleep(3600, loop=loop)


async def setup_recurring_gnews_scrape():
    while True:
        logging.info('Querying Google News API...')
        # Will need to incorporate a service to create word combinations
        placeholder = ['Trump']
        await query_google(create_google_news_url(placeholder))
        await asyncio.sleep(3600, loop=loop)


def setup_app():
    app = connexion.AioHttpApp(__name__, specification_dir='swagger/')
    app.add_api('api.spec.yaml', resolver=RestyResolver('api'))
    return app


async def setup_db():
    app = {}
    await init_db()
    app['db'] = db
    return app


if __name__ == '__main__':
    logging.info('Beginning app startup...')
    logging.info(f'Using API_PORT: {API_PORT}')
    logging.info(f'Using FORBIDDEN_WORDS: {FORBIDDEN_WORDS}')

    logging.info('Setting up RESTapi...')
    app = setup_app()

    logging.info('Initializing Database...')
    loop.create_task(init_db())

    logging.info('Starting NewsAPI Webscraping Task...')
    loop.create_task(setup_recurring_newsapi_scrape())

    logging.info('Starting Google News Webscraping Task...')
    loop.create_task(setup_recurring_gnews_scrape())

    app.run(port=API_PORT)