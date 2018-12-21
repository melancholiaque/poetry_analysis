import re
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from .models import Poem


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


def clean(string):
    for char in ['\r', '\n', '-', ',', '.', ';']:
        string = string.replace(char, ' ')
    return re.sub('\s+', ' ', string)


def predict(string):
    return le.inverse_transform(rfc.predict(
        pca.transform(vec.transform([ps.stem(clean(string))]))))
