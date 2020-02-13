import os
import csv
import logging
import asyncio
import requests

from utils import setup_db
from model import db, NewsArchive

logging.basicConfig(level=logging.INFO)


OUTPUT_PATH = os.environ.get('OUTPUT_PATH', '.')
API_KEY = os.getenv('API_KEY')
API_HOST = 'japerk-text-processing.p.rapidapi.com'
loop = asyncio.get_event_loop()


class CorpusParser():

    def __init__(self, db, table):
        self.url = 'https://japerk-text-processing.p.rapidapi.com/sentiment/'
        self.db = db
        self.table = table
        self.corpus = []

    def __auth(self):
        return { 'x-rapidapi-host': API_HOST, 'x-rapidapi-key': API_KEY }

    def __post(self, desc):
        logging.info(f'POSTing with {desc}')
        response = requests.post(self.url, {'text': desc}, headers=self.__auth())
        assert response.status_code == 200, \
            f'Response status {response.status_code} is not 200, ' \
            f'raised error: {" ".join([f"{k.upper()}: {v}" for k, v in response.json().items()])}'
        return (response.json(), desc)

    def __export(self):
        logging.info(f'Exporting corpus: {self.corpus}')
        with open(OUTPUT_PATH + '/corpus.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=['description', 'pos', 'neutral', 'neg']
            )
            for sentiment in self.corpus:
                description = sentiment[1].replace(',', '')
                print(description)
                writer.writerow({
                    'description': description,
                    'pos': str(sentiment[0]['probability']['pos']),
                    'neutral': str(sentiment[0]['probability']['neutral']),
                    'neg': str(sentiment[0]['probability']['neg'])
                })
                csvfile.flush()

    async def __call__(self):
        logging.info('Acquiring articles...')
        async with self.db.bind.acquire() as conn:

            articles = await conn.all(self.table.query.distinct('url'))
            article_dump = [article.dump() for article in articles]

        count = 0
        for article in article_dump:
            if count < 100:
                self.corpus.append(self.__post(article['description']))
            count += 1

        self.__export()


if __name__ == '__main__':
    logging.info('Setup Database Connection...')
    loop.run_until_complete(setup_db())

    logging.info('Initialize Command...')
    parser = CorpusParser(db, NewsArchive)

    loop.run_until_complete(parser())