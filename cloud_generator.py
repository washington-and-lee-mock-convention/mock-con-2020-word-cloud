import nltk
from nltk import word_tokenize
nltk.download(['punkt', 'averaged_perceptron_tagger'])


class WordCloudGenerator:

    def __init__(self, threshold):
        self.threshold = threshold


    def _count_words(self, text):
        dictionary = {}
        buzzwords = []
        for (word, tag) in nltk.pos_tag(word_tokenize(text)):
            if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1
        return dictionary
        

    def __call__(self, text):
        return self._count_words(text)