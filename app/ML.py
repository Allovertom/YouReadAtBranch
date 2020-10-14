from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
import math
from sklearn import svm
from sklearn.metrics import f1_score

def learning(all_courpus_ls):
    ###特徴量Xの作成
    #all_courpus_lsを１次元化
    #https://note.nkmk.me/python-numpy-ndarray-slice/にて実施
    vectorizer = TfidfVectorizer(stop_words='english')#英語のストップワード除去
    X = vectorizer.fit_transform(all_courpus_ls)


    ###正解データYの作成
    #https://note.nkmk.me/python-numpy-ndarray-slice/にて実施




    ###学習
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    ###Liner svc
    para = {'C':[10 ** i for i in range(-5, 6)]}
    svc = svm.SVC(kernel='linear')
    clf = GridSearchCV(svc, para)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score = f1_score(y_test, y_pred, average=None)

    #GridserchCVでパラメ調整
    

    ###Naive bayes
    #GridserchCVでパラメ調整
    

    
"""     ###決定木
    #GridserchCVでパラメ調整
    para = {"min_samples_split":range(5,len(X_train),math.floor(len(X_train)/4)), "criterion":("gini","entropy")}
    tre = DecisionTreeClassifier()
    clf = GridSearchCV(tre, para)
    clf = clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test) """




    return score


