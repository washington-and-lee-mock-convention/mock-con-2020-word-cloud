import requests
import asyncio
import aiohttp
import logging
from datetime import datetime
from dateutil import parser
from concurrent.futures import ALL_COMPLETED
from model import db, WordCloud

logging.basicConfig(level=logging.INFO)

class WebCourier:
    '''
    This class will open a requests session and make a request to the given url.
    The resultant json will be scrubbed for body text and the text will be fed through
    the word count class which will return a dict of word to number of occurences.
    The courier will then make the async database transaction with the correct model
    '''

    def __init__(self, loop, cloud_generator):
        self.loop = loop
        self.session = aiohttp.ClientSession()
        self.cloud_generator = cloud_generator


    async def _fetch(self, url):
        async with self.session.get(url) as resp:
            status = resp.status
            logging.info(f"Received status {status} from Google API.")
            assert status == 200
            return await resp.json()


    async def __call__(self, url):
        task = [self._fetch(url)]
        done, pending = await asyncio.wait(
            task,
            loop=self.loop,
            return_when=ALL_COMPLETED
        )
        for task in done:
            data = task.result()
            for article in data['articles']:
                content = article['description']
                date_published = parser.parse(article['publishedAt']).replace(tzinfo=None)
                words_to_frequency = self.cloud_generator(content)

                for word in words_to_frequency.keys():
                    sanitized_word = {
                        'word': word,
                        'date_published': date_published,
                        'date_recorded': datetime.utcnow()
                    }

                async with db.transaction():
                    word_to_create = WordCloud(**sanitized_word)
                    created_word = await word_to_create.create()
                    dump = created_word.dump()
                    logging.info(f"DB Transaction {created_word} - {dump}")
                    dump['date_published'] = str(dump['date_published'])
                    dump['date_recorded'] = str(dump['date_recorded'])


    def __del__(self):
        self.session.close()