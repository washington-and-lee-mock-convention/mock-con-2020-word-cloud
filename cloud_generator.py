class WordCloudGenerator:

    def __init__(self, forbidden_words):
        self.forbidden_words = forbidden_words
        self.accepted_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', \
        'w', 'x', 'y', 'z']

    def _count_words(self, text):
        # define word to count map
        word_to_count = {}

        # create list of words (with punctuation)
        text_list = text.split(' ')
        scrubbed_text_list = list()

        # remove punction
        for word in text_list:
            word = list(word.lower())
            for char in word:
                if char not in self.accepted_symbols:
                    word.remove(char)
            scrubbed_text_list.append("".join(word))

        # count words
        for word in scrubbed_text_list:
            if word in forbidden_words:
                break
            if word not in word_to_count:
                word_to_count[word] = 1
            else:
                word_to_count[word] += 1

        return word_to_count

    def __call__(self, text):
        return self._count_words(text)