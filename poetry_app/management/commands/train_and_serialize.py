from django.core.management.base import BaseCommand, CommandError
from ...models import Poet, Poem
from ...services import pipeline
from os.path import splitext

import numpy as np
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


class Command(BaseCommand):

    help = 'trains and serializes model by path'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str,
                            help='.pkl file to serialize to')

    def handle(self, *args, **options):
        path = options.get('path', None)
        ps = PorterStemmer()
        le = LabelEncoder()
        pca = TruncatedSVD(n_components=150)
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

        y = le.fit_transform(poets)
        X = vec.fit_transform(content)
        X = pca.fit_transform(X)

        svm.fit(X, y)
        mlp.fit(X, y)
        rfc.fit(X, y)
        vc.fit(X, y)

        pipe = pipeline(ps, vec, pca, vc, le)
        pipe.dump_to(path)
