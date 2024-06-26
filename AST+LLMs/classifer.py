
import os
import torch
from sklearn.metrics import accuracy_score
from sklearn import metrics
import datetime
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
import joblib
import pandas as pd
import pickle as cPickle

print(torch.cuda.is_available())
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

def ListToCSV(list_to_csv, path):
    df = pd.DataFrame(list_to_csv)
    df.to_csv(path, index=False)
def load_pickle(file_to_load):
    with open(file_to_load, 'rb') as module_to_load:
        obj_name = cPickle.load(module_to_load)
    return obj_name

# load gnn-train
train_repre = load_pickle("train_repre.pkl")
train_y = load_pickle("train_set_y.pkl")
train_id = load_pickle("train_set_id.pkl")
print(len(train_repre))
print(len(train_y))
print(len(train_id))


#load gnn-val
val_repre = load_pickle("validation_repre.pkl")
val_y = load_pickle("validation_set_y.pkl")
val_id = load_pickle("validation_set_id.pkl")
print(len(val_repre))
print(len(val_y))
print(len(val_id))

# load gnn-test
test_repre = load_pickle("test_repre.pkl")
test_y = load_pickle("test_set_y.pkl")
test_id = load_pickle("test_set_id.pkl")
print(len(test_repre))
print(len(test_y))
print(len(test_id))


X_train = train_repre+val_repre
X_test = test_repre
y_train = train_y+val_y
y_test = test_y
import time
import pickle
import numpy as np
from numpy import genfromtxt
import pandas as pd
from itertools import chain
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
def invokeRandomForest(train_set_x, train_set_y, test_set_x, test_set_y):
    #    param_grid = {'max_depth': [15,20,25,30],
    #                  'min_samples_split': [4,5,6],
    #                  'min_samples_leaf': [2,3,4,5],
    #                  'bootstrap': [True,False],
    #                  'criterion': ['gini','entropy'],
    #                  'n_estimators': [40,50,55,60,65]}
    #
    train_set_y = np.ndarray.flatten(np.asarray(train_set_y))
    test_set_y = np.ndarray.flatten(np.asarray(test_set_y))
    output_dir ='/home/mxy/yx/liiin/Graph_represenations/data/results'

    # clf = GridSearchCV(RandomForestClassifier(), param_grid=param_grid, n_jobs=-1)
    clf = RandomForestClassifier(bootstrap=True, class_weight='balanced',  # class_weight={0:1, 1:4},
                                 criterion='entropy', max_depth=40, max_features='auto',
                                 max_leaf_nodes=None, min_impurity_decrease=0.0,
                                 #min_impurity_split=None, min_samples_leaf=3,
                                 min_samples_leaf=3,
                                 min_samples_split=4, min_weight_fraction_leaf=0.0,
                                 n_estimators=8000, oob_score=False, random_state=None,
                                 verbose=1, warm_start=False, n_jobs=-1)
    clf = clf.fit(train_set_x, train_set_y)

    print("feature importance:")
    #print(clf.feature_importances_)
    print("\n")

    # print("best estimator found by grid search:")
    # print(clf.best_estimator_)

    print("\r\n")

    # evaluate the model on the test set
    print("predicting on the test set")
    # t0 = time()
    y_predict = clf.predict(test_set_x)

    y_predict_proba = clf.predict_proba(test_set_x)[:,0]

    # Accuracy
    accuracy = np.mean(test_set_y == y_predict) * 100
    print("accuracy = " + str(accuracy))

    target_names = ["Non-vulnerable", "Vulnerable"]  # non-buggy->0, buggy->1
    print(confusion_matrix(test_set_y, y_predict, labels=[0, 1]))
    print("\r\n")
    print("\r\n")
    print(classification_report(test_set_y, y_predict, target_names=target_names))
    ######################

    zippedlist = list(zip(y_predict_proba, test_y))
    result_set = pd.DataFrame(zippedlist, columns=['Probs. of being vulnerable', 'Label'])
    ListToCSV(result_set, output_dir + os.sep +  '_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '_result.csv')
invokeRandomForest(X_train, y_train, X_test, y_test)

