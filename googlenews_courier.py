import requests
import asyncio
import aiohttp
import logging
from datetime import datetime
from dateutil import parser
from concurrent.futures import ALL_COMPLETED
from model import db, NewsArchive
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

class GoogleNewsCourier:

    def __init__(self, loop):
        self.loop = loop
        self.session = aiohttp.ClientSession()

    
    def get_string(self, tag):
        return tag.getText()


    def get_link_from_description(self, description):
        description = str(description)
        desc_list = description.split()
        for item in desc_list:
            if 'href' in item:
                return item[6:len(item) - 1] #remove href=''
        return None


    async def _fetch(self, url):
        async with self.session.get(url) as resp:
            status = resp.status
            logging.info(f"Received status {status} from Google API.")
            assert status == 200
            return await resp.text()


    async def __call__(self, url):
        task = [self._fetch(url)]
        done, pending = await asyncio.wait(
            task,
            loop=self.loop,
            return_when=ALL_COMPLETED
        )
        for task in done:
            data = task.result()
            tree = BeautifulSoup(data, 'lxml')

            body = tree.body

            for item in body.find_all(name='item'):
                for title, link, date in zip(
                    item.find_all(name='title'),
                    item.find_all(name='description'),
                    item.find_all(name='pubdate')
                ):
                    title = self.get_string(title)
                    link = self.get_link_from_description(link)
                    date = self.get_string(date)

                    if None in [title, link, date]:
                        logging.info(f'Missing one or more keys')
                        break
                    
                    sanitized_newsfeed = {
                        'description': title,
                        'url': link,
                        'date_published': parser.parse(date).replace(tzinfo=None),
                        'date_recorded': datetime.utcnow()
                    }

                    async with db.transaction():
                        news_to_add = NewsArchive(**sanitized_newsfeed)
                        added_news = await news_to_add.create()
                        dump = added_news.dump()
                        logging.info(f"DB Transaction {added_news} - {dump}")
                        dump['date_published'] = str(dump['date_published'])
                        dump['date_recorded'] = str(dump['date_recorded'])
        


    def __del__(self):
        self.session.close()