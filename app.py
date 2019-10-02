import os
import asyncio
import connexion
import logging
from connexion.resolver import RestyResolver
from web_courier import WebCourier
from cloud_generator import WordCloudGenerator

API_PORT = os.environ.get('API_PORT', 8080)
FORBIDDEN_WORDS = os.environ.get('FORBIDDEN_WORDS', [])
logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

query_web = WebCourier(loop, 'temp_url', WordCloudGenerator(FORBIDDEN_WORDS))


async def setup_recurring_web_scrape():
    await query_web()


def setup_app():
    app = connexion.AioHttpApp(__name__, specification_dir='swagger/')
    app.add_api('api.spec.yaml', resolver=RestyResolver('api'))
    return app

if __name__ == '__main__':
    logging.info('Beginning app startup...')
    logging.info(f'Using API_PORT: {API_PORT}')
    logging.info(f'Using FORBIDDEN_WORDS: {FORBIDDEN_WORDS}')

    logging.info('Setting up RESTapi...')
    app = setup_app()

    logging.info('Starting Webscraping Task...')
    loop.create_task(setup_recurring_web_scrape())

    app.run(port=API_PORT)