from django.core.management.base import BaseCommand, CommandError
from ...models import Poet, Poem
from ...services import pipeline
from os.path import splitext

import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class Command(BaseCommand):

    help = 'trains and serializes model by path'

    def add_arguments(self, parser):
        parser.add_argument('threshold', type=int, nargs='?', default=0,
                            help='balance classes with threshold')

    def handle(self, *args, **options):
        thre = options.get('threshold', None)
        ps = PorterStemmer()
        svd = TruncatedSVD(n_components=500)
        le = LabelEncoder()
        vec = TfidfVectorizer()

        rfc = RandomForestClassifier(n_estimators=150, criterion='gini')
        mlp = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000)
        svm = SVC(kernel='rbf', C=2, gamma=2)
        estimators = [
            ('svm', svm),
            ('mlp', mlp),
            ('rfc', rfc)
        ]
        vc = VotingClassifier(estimators=estimators, voting='hard')

        poems = Poem.objects.all()
        content = np.array([p.content for p in poems])
        poets = np.array([p.poet.name for p in poems])

        df = pd.DataFrame(data={'author': poets, 'content': content})

        if thre:
            authors = df['author'].unique()
            dist = [(a, (df['author'] == a).sum()) for a in authors]
            droplist = [a for a, i in dist if i < thre]
            mask = df['author'].apply(lambda x: x not in droplist)
            thre_df1 = df[mask]
            take_list = [a for a, i in dist if i > thre]
            author_series, content_series = [], []
            for a in take_list:
                author_series += [a] * thre
                content_series += (df[df['author'] == a]['content']
                                   .iloc[:thre].tolist())
            thre_df2 = pd.DataFrame(data={'author': author_series,
                                          'content': content_series})
            df = pd.concat([thre_df1, thre_df2])
        print(f'{len(np.unique(df["author"]))} unique poets')

        poets = df['author']
        poems = df['content']

        y = le.fit_transform(poets)
        X = vec.fit_transform(poems)
        X = svd.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.3)

        svm.fit(X_train, y_train)
        mlp.fit(X_train, y_train)
        rfc.fit(X_train, y_train)
        vc.fit(X_train, y_train)

        print(f'accuracy_score: {accuracy_score(vc.predict(X_test), y_test)}')

        svm.fit(X, y)
        mlp.fit(X, y)
        rfc.fit(X, y)
        vc.fit(X, y)

        pipe = pipeline(ps, vec, svd, vc, le)
        pipe.dump_to('pickled_objects/estimator.pkl')
