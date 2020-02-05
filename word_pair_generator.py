import random
import logging
import asyncio
from itertools import chain, combinations

from model import WordCloud

logging.basicConfig(level=logging.INFO)


class Generator:

    def __init__(self, seed, max_size):
        self.salt = list(seed)
        self.max_query_size = max_size
        self.num_queries = 25

    async def get_words(self, db):
        words_to_freq = await db.select([
            WordCloud.word,
            db.func.count(db.func.distinct(WordCloud.source))
        ]).group_by(
            WordCloud.word
        ).gino.all()

        return {k: v for k, v in words_to_freq if v is not None}

    def _get_rand_salt(self):
        return self.salt[random.randint(0, len(self.salt) - 1)]

    async def _create_permutations_list(self, db):

        def powerset(iterable):
            s = list(iterable)
            return chain.from_iterable(
                combinations(s, r) for r in range(self.max_query_size + 1)
            )

        def compute_sample_frequency(words, repr_set):
            ''' Computes the mean frequency of the word sample '''
            frequencies = [words[word] for word in repr_set]
            return sum(frequencies)/ len(repr_set)

        # set the number of word in set as 30 to maintain distribution
        words_to_freq = await self.get_words(db)
        words_freq = list(words_to_freq.values())
        words_list = list(words_to_freq.keys())
        average_frequency = sum(words_freq) / len(words_list)
        repr_set_words = []
        while True:
            if len(words_list) > 30:
                repr_set_words = [words_list[random.randint(0, len(words_list) - 1)] for _ in range(30)]
            else:
                repr_set_words = words_list

            if compute_sample_frequency(words_to_freq, repr_set_words) >= average_frequency:
                break

        query_set = set(powerset(repr_set_words))

        subset = []
        i = 0
        query_set = list(query_set)
        # Reduce number of requests using random selection
        while i < self.num_queries:
            query = query_set[random.randint(0, len(query_set) - 1)] + (self._get_rand_salt(),)
            subset.append(query)
            i += 1
        
        return set(subset)

    def __call__(self, loop, db):
        return loop.create_task(
            self._create_permutations_list(db)
        )
