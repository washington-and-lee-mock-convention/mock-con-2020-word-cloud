import requests
import asyncio
import aiohttp


class WebCourier:
    '''
    This class will open a requests session and make a request to the given url.
    The resultant json will be scrubbed for body text and the text will be fed through
    the word count class which will return a dict of word to number of occurences.
    The courier will then make the async database transaction with the correct model
    '''

    baseURL = 'https://google.com/search?q='

    def __init__(self, loop, url, cloud_generator):
        self.url = url
        self.loop = loop
        self.session = aiohttp.ClientSession()
        self.cloud_generator = cloud_generator

    async def __call__(self):
        pass

    def __del__(self):
        self.session.close()