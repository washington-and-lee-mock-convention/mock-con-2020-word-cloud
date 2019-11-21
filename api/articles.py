import responses
from sqlalchemy import literal
from model import db, NewsArchive


async def search(*args, **kwargs):

    articles = []
    articles_dump = None
    search = None

    if 'search' in kwargs:
        search = str(kwargs['search'])
    
    async with db.bind.acquire() as conn:

        query = NewsArchive.query

        if search:
            words = search.split(' ')
            for word in words:
                query.append_whereclause(
                    NewsArchive.description.contains(word)
                )

        articles_count = await conn.scalar(query.alias().count())

        query = query.limit(
                    kwargs['page_size']
                ).offset(
                    kwargs['page'] * kwargs['page_size']
                ).order_by(
                    NewsArchive.date_published.desc()
                )

        articles = await conn.all(query)

    if articles is None:
        return responses.not_found()
    else:
        article_dump = [article.dump() for article in articles]
        return responses.search(articles_count, article_dump)
