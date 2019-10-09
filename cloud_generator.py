class WordCloudGenerator:

    def __init__(self, forbidden_words, threshold):
        self.forbidden_words = forbidden_words
        self.threshold = threshold


    def _count_words(self, text):
        dictionary = {}
        buzzwords = []
        for word in text.split(' '):
            if((word.lower() not in self.forbidden_words) and (word.isalnum())):
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1
        # for item in dictionary:
        #     if dictionary[item] >= self.threshold:
        #         buzzwords.append(item)
        # return buzzwords
        return dictionary
        

    def __call__(self, text):
        return self._count_words(text)