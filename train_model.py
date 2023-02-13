#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 22:08:39 2020
Script to run Voting Classifier on the Featurised Dataset

@author: aakanksha
"""
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from sklearn.model_selection import StratifiedKFold
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report 
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import average_precision_score
from matplotlib import pyplot
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
#from sklearn.utils.fixes import signature
from sklearn.metrics import average_precision_score
from sklearn.metrics import fbeta_score
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
import pickle


#scoring = ['precision_macro', 'recall_macro', 'accuracy']

scoring = {'accuracy' : make_scorer(accuracy_score), 
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score), 
           'f1_score' : make_scorer(f1_score)}



df_train = pd.read_csv('/feature_file.csv', encoding = "ISO-8859-1")

d={'N':0, 'P': 1}

y_train = df_train['Label'].map(d)

X_train = df_train.drop(['Label', 'Secret', '.Count', 'File', 'Repo Name', 'Line', 'Entropy', 'Does username exists in 5 lines up pr down?'], axis = 1)
print(X_train.head)

for col in X_train.columns: 
    print(col)
    


for col in X_train.columns:
    X_train[col] = X_train[col].astype('category')
    X_train[col] = X_train[col].cat.codes + 1
    
    
  
print(X_train.shape)

#clf1 = LogisticRegression(solver='lbfgs', multi_class='multinomial',random_state=42)
clf1 = LogisticRegression(solver='liblinear',random_state=42, C = 3.0)
clf2= GaussianNB()
clf3 = SVC(gamma='auto', C = 2.0, tol = 0.001, probability=True)
#clf3 = SVC(gamma='auto', C= 2.0,tol=0.1, probability=True)


clf = VotingClassifier(estimators=[('lg', clf1) ,('gb', clf2), ('svc', clf3)], voting='soft', weights=[1,1,1])
clf.fit(X_train, y_train)
'''    
scores = cross_validate(clf, X_train, y_train, scoring=scoring, cv=StratifiedKFold(4), return_train_score=False)
print("Precision: " ,scores['test_precision'])
print("Average Precision:", sum(scores['test_precision']) / len(scores['test_precision'])) 
print("Recall: " ,scores['test_recall'])
print("Average Recall:", sum(scores['test_recall']) / len(scores['test_recall'])) 
print("F1score: " ,scores['test_f1_score'])
print("Average F1score:", sum(scores['test_f1_score']) / len(scores['test_f1_score'])) 
#print("Fbetascore: " ,scores['test_fbeta_score'])
#print("Average Fbeta score:", sum(scores['test_fbeta_score']) / len(scores['test_fbeta_score'])) 
    
'''

y_pred = clf.predict(X_train)
print(classification_report(y_train, y_pred))

cm = confusion_matrix(y_train, y_pred)
print(cm)

fbeta = fbeta_score(y_train, y_pred, 2)
print("Fbeta:", fbeta)
f1 = f1_score(y_train, y_pred)
print("F1:", f1)
precision = precision_score(y_train, y_pred)
print("Precision: ", precision)
recall = recall_score(y_train, y_pred)
print("Recall:", recall)

pickle.dump([clf, fbeta, f1, precision, recall], open('complete_ml.pkl', 'wb'))




