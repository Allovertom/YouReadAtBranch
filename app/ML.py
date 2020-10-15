from nltk.tokenize import word_tokenize #nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
import math
from sklearn import svm
from sklearn.metrics import f1_score
import numpy as np
from nltk.stem.snowball import SnowballStemmer


class SnowballTokenizer(object):
    def __init__(self):
        self.snowball = SnowballStemmer("english")
        
    def __call__(self, doc):
        return [self.snowball.stem(w) for w in word_tokenize(doc)]

def learning(all_courpus_ls):
    ###特徴量Xの作成
    all_ndarr = np.array(all_courpus_ls)#ndarrayに変換
    X_corpus = all_ndarr[:, 0]#文章のみスライスで切り出し
    y_arr_3d = all_ndarr[:, 1:]#教師データのみスライスできり出し
    Y_3d = y_arr_3d.astype(int)*np.array([1,2,3])#カラム毎に番号付与
    Y = Y_3d.max(axis=1)#1次元化

    #英語のストップワード除去, SnowballTokenizer()でTokenizeとstemmingを同時に行う。
    vectorizer = TfidfVectorizer(stop_words='english', tokenizer=SnowballTokenizer())
    X = vectorizer.fit_transform(X_corpus)

    ###学習
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    ###Liner svc
    para = {'C':[10 ** i for i in range(-1, 6)]}
    svc = svm.SVC(kernel='linear')
    clf = GridSearchCV(svc, para)
    try:
        clf.fit(X_train, y_train)
    except ValueError:
        print("学習データが足りません。")
    y_pred = clf.predict(X_test)
    score = f1_score(y_test, y_pred, average=None)
    #GridserchCVでパラメ調整
    ###Naive bayes
    #GridserchCVでパラメ調整
    ###決定木
    #GridserchCVでパラメ調整
    #para = {"min_samples_split":range(5,len(X_train),math.floor(len(X_train)/4)), "criterion":("gini","entropy")}
    #tre = DecisionTreeClassifier()
    #clf = GridSearchCV(tre, para)
    #clf = clf.fit(X_train, y_train)
    #acc = clf.score(X_test, y_test)
    return score


