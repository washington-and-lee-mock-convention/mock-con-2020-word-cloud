import os
import asyncio
import connexion
import logging
import aiohttp_cors
from connexion.resolver import RestyResolver
from newsapi_courier import NewsAPICourier
from cloud_generator import WordCloudGenerator
from googlenews_courier import GoogleNewsCourier
from word_pair_generator import Generator
from utils import (
    create_newsapi_url, create_google_news_url,
    word_seed, setup_db
)

API_PORT = os.environ.get('PORT', 8080)
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY', '7250f963ffc04ab0bf82535a74c91358')
THRESHOLD = os.environ.get('THRESHOLD', 0)
MAX_QUERY_SIZE = os.environ.get('MAX_QUERY_SIZE', 3)

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

generator = Generator(word_seed(), MAX_QUERY_SIZE)
query_newsapi = NewsAPICourier(loop, WordCloudGenerator(THRESHOLD), generator)
query_google = GoogleNewsCourier(loop)


async def setup_recurring_newsapi_scrape(db):
    while True:
        queries = await generator(loop, db)
        logging.info(f'Querying News API with queries: {queries}')
        for query in queries:
            await query_newsapi(create_newsapi_url(query, NEWSAPI_KEY))
        await asyncio.sleep(6400, loop=loop)


async def setup_recurring_gnews_scrape(db):
    while True:
        queries = await generator(loop, db)
        logging.info(f'Querying Google News API with queries: {queries}')
        for query in queries:
            await query_google(create_google_news_url(query))
        await asyncio.sleep(60, loop=loop)


def setup_app():
    app = connexion.AioHttpApp(__name__, specification_dir='swagger/')
    app.add_api('api.spec.yaml', resolver=RestyResolver('api'))

    cors = aiohttp_cors.setup(app.app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "PUT"]
        )
    })
    for route in list(app.app.router.routes()):
        cors.add(route)

    return app


if __name__ == '__main__':
    logging.info('Beginning app startup...')
    logging.info(f'Using API_PORT: {API_PORT}')

    logging.info('Setting up RESTapi...')
    app = setup_app()

    logging.info('Initializing Database...')
    db = loop.run_until_complete(setup_db())['db']

    logging.info('Starting NewsAPI Webscraping Task...')
    loop.create_task(setup_recurring_newsapi_scrape(db))

    logging.info('Starting Google News Webscraping Task...')
    loop.create_task(setup_recurring_gnews_scrape(db))

    app.run(port=API_PORT)