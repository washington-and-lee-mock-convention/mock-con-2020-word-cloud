import responses
from sqlalchemy import literal
from model import db, NewsArchive


async def search(*args, **kwargs):

    articles = []
    articles_dump = None
    keyword = None

    if 'keyword' in kwargs:
        keyword = str(kwargs['keyword'])
    
    async with db.bind.acquire() as conn:

        query = NewsArchive.query

        if keyword:
            query.append_whereclause(
                NewsArchive.description.contains(keyword)
            )

        articles = await conn.all(query)

    if articles is None:
        return responses.not_found()
    else:
        article_dump = [article.dump() for article in articles]
        return responses.get(article_dump)