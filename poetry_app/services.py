import pickle
import re


class pipeline:

    def __init__(self, stemmer, vec, svd, vc, le):
        self.stemmer = stemmer
        self.vec = vec
        self.svd = svd
        self.vc = vc
        self.le = le

    def predict(self, poem):
        pp = self.stemmer.stem(self.clean(poem))
        val = self.svd.transform(self.vec.transform([f'{pp} ']))
        return self.le.inverse_transform(self.vc.predict(val))

    def clean(self, string):
        for char in ['\r', '\n', '-', ',', '.', ';', '(', ')']:
            string = string.replace(char, ' ')
        return re.sub('\s+', ' ', string)

    def dump_to(self, path):
        with open(path, 'wb') as fd:
            pickle.dump(self, fd, pickle.DEFAULT_PROTOCOL)

    @staticmethod
    def load_from(path):
        with open(path, 'rb') as fd:
            obj = pickle.load(fd, )
        return obj
