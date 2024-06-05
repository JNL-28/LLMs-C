
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
output_dir='/home/mxy/yx/liiin/Graph_represenations/data/results'
zippedlist = list(zip(test_id, y_test))
result_set = pd.DataFrame(zippedlist, columns=['id','label'])
ListToCSV(result_set, output_dir + os.sep +  '_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ 'test_result.csv')
