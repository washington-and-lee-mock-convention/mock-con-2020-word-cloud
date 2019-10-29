import random
from itertools import chain, combinations

class Generator:

    def __init__(self, seed, max_size):
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

    def _create_permutations_list(self):

        def powerset(iterable):
            s = list(iterable)
            return chain.from_iterable(
                combinations(s, r) for r in range(self.max_query_size + 1)
            )

        query_set = set(powerset(self.words.keys()))

        subset = []
        i = 0
        query_set = list(query_set)
        ## Reduce number of requests using random selection
        while i < self.num_queries:
            subset.append(
                query_set[random.randint(0, len(query_set))]
            )
            i += 1
        
        return set(subset)

    def __call__(self):
        return self._create_permutations_list()
