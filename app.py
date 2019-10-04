import os
import asyncio
import connexion
import logging
from connexion.resolver import RestyResolver
from web_courier import WebCourier
from cloud_generator import WordCloudGenerator
from model import init_db, db

API_PORT = os.environ.get('API_PORT', 8080)
FORBIDDEN_WORDS = os.environ.get('FORBIDDEN_WORDS', [])
logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

query_web = WebCourier(loop, 'temp_url', WordCloudGenerator(FORBIDDEN_WORDS))


async def setup_recurring_web_scrape():
    '''
        This should be set to run each hour and iterate over each of the given key words.
        Need to consider what key word pairs are going to be important and how we can generate
        key words based on findings. We don't want to necessarily feed our model with the most
        used words from already scanned documents because this will cause bias in the output.
    '''
    while True:
        logging.info('Querying Google Search API...')
        await query_web()
        await asyncio.sleep(60, loop=loop)


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

    logging.info('Starting Webscraping Task...')
    loop.create_task(setup_recurring_web_scrape())

    app.run(port=API_PORT)