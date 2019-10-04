import os
from gino import Gino
db = Gino()

db_user = os.environ.get('DB_USER', 'wordcloud')
db_password = os.environ.get('DB_PASSWORD', 'wordcloud')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME', 'wordcloud')


async def init_db():
    await db.set_bind('postgresql://{}:{}@{}:{}/{}'.format(db_user,
                                                           db_password,
                                                           db_host,
                                                           db_port,
                                                           db_name))


async def disconnect():
    db.pop_bind().close()


class WordCloud(db.Model):
    __tablename__ = 'wordcloud'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.Unicode)
    date_published = db.Column(db.DateTime(timezone=True), server_default="timezone('utc'::text, now())")
    date_recorded = db.Column(db.DateTime(timezone=True), server_default="timezone('utc'::text, now())")

    def dump(self):
        return {k: v for k, v in self.__values__.items() if v is not None}