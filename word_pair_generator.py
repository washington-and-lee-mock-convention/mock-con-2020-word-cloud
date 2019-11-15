import random
import logging
from itertools import chain, combinations

logging.basicConfig(level=logging.INFO)

class Generator:

    def __init__(self, seed, max_size):
        self.salt = list(seed)
        self.words = {k: 1 for k in seed}
        self.max_query_size = max_size
        self.num_queries = 25

    def add_words(self, words):
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def get_words(self):
        return self.words

    def _get_rand_salt(self):
        return self.salt[random.randint(0, len(self.salt) - 1)]

    def _create_permutations_list(self):

        def powerset(iterable):
            s = list(iterable)
            return chain.from_iterable(
                combinations(s, r) for r in range(self.max_query_size + 1)
            )

        def compute_sample_frequency(words):
            ''' Computes the mean frequency of the word sample '''
            frequencies = [self.words[word] for word in words]
            return sum(frequencies)/ len(words)

        # set the number of word in set as 30 to maintain distribution
        words_list = list(self.words.keys())
        average_frequency = sum(list(self.words.values())) / len(words_list)
        repr_set_words = []
        while True:
            if len(words_list) > 30:
                repr_set_words = [words_list[random.randint(0, len(self.words) - 1)] for _ in range(30)]
            else:
                repr_set_words = words_list

            if compute_sample_frequency(repr_set_words) >= average_frequency:
                break

        query_set = set(powerset(repr_set_words))

        subset = []
        i = 0
        query_set = list(query_set)
        # Reduce number of requests using random selection
        while i < self.num_queries:
            query = query_set[random.randint(0, len(query_set))] + (self._get_rand_salt(),)
            subset.append(query)
            i += 1
        
        return set(subset)

    def __call__(self):
        logging.info(f'Beginning permutations generation with words: {self.words}')
        return self._create_permutations_list()
