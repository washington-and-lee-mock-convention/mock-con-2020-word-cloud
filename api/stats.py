import json
import responses
import logging
import operator
from sqlalchemy import func
from model import db, WordCloud

logging.basicConfig(level=logging.INFO)


async def search(*args, **kwargs):

    logging.info(f'Recieved {kwargs}')

    stat_funcs = {
        'most_used_word': _get_most_used_word,
        'word_frequency': _get_word_frequency,
    }
    func = stat_funcs[kwargs['stat']]
    params = {}

    query = WordCloud.query

    words = await query.gino.all()
    words_dump = [word.dump() for word in words]
    params['words'] = words_dump
    if words is None:
        return responses.not_found()
    else:
        response = await func(params)
        return responses.get(response)


async def _get_most_used_word(params):

    def _get_frequency_dict(words):
        dictionary = {}
        for word in words:
            if word in dictionary.keys():
                dictionary[word] += 1
            else:
                dictionary[word] = 1
        return dictionary

    db_rows = params['words']
    words = [row['word'] for row in db_rows]
    freq_dict = _get_frequency_dict(words)
    
    most_frequent = max(freq_dict.items(), key=operator.itemgetter(1))[0]
    return {'most_used_word': most_frequent}


async def _get_word_frequency(params):

    words_to_freq = await db.select(
        [
            WordCloud.word,
            db.func.count(db.func.distinct(WordCloud.source))
        ]
    ).group_by(
        WordCloud.word
    ).gino.all()

    return [{k: v for k, v in words_to_freq if v is not None}]