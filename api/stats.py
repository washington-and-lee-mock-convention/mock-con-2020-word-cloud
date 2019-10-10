import json
import responses
import logging
import operator
from model import db, WordCloud

logging.basicConfig(level=logging.INFO)


async def search(*args, **kwargs):

    logging.info(f'Recieved {kwargs}')

    stat_funcs = {'most_used_word': _get_most_used_word}
    func = stat_funcs[kwargs['stat']]
    params = {}

    query = WordCloud.query

    words = await query.gino.all()
    words_dump = [word.dump() for word in words]
    params['words'] = words_dump
    if words is None:
        return responses.not_found()
    else:
        return responses.get(func(params))


def _get_most_used_word(params):

    def _get_frequency_dict(words):
        dictionary = {}
        for word in words:
            print(word)
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