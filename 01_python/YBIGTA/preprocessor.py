class TextPreprocessor:
    def __init__(self, texts):
        self.texts = texts
        self.corpus = self._preprocess_texts()

    def _preprocess_texts(self):
        corpus = {}

        for text in self.texts:
            text = text.replace('\n', '')
            words = text.split()

            for word in words:
                word_processed = ' '.join(list(word.lower())) + ' </w>'
                
                if word_processed in corpus:
                    corpus[word_processed] += 1
                else:
                    corpus[word_processed] = 1

        return corpus

    def get_corpus(self):
        print(self.corpus)
        return self.corpus