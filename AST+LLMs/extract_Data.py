import os
floder = '/home/mxy/yx/data/data_Test/'
floder_list = os.listdir(floder)
print(floder_list)
import io


def extra_data(filename):
    data = []
    with io.open(filename, 'r', encoding='windows-1252') as file:
        line = file.readline()
        while line:
            if line == "\n":
                line = file.readline()
                continue
            line = line.replace("\n", "").replace("  ", "").replace("\t", "")
            data.append(line)
            line = file.readline()

    return " ".join(data)
idx=100000
all_data=[]
for i in floder_list:
    print(i)
    #if i !='FFmpeg':
    filename = floder+i+"/"+"Non_vulnerable_functions/"
    for j in os.listdir(filename):
        files = filename+j
        data_dic  = {}
        data_dic['func'] =  extra_data(files)
        data_dic['target'] =  0
        data_dic['idx'] =  idx
        data_dic['project'] =  i
        idx+=1
        all_data.append( data_dic )

    filename =  floder+i+"/"+"Vulnerable_functions/"
    for j in os.listdir(filename):
        files = filename+j
        data_dic  = {}
        data_dic['func'] = extra_data(files)
        data_dic['target'] = 1
        data_dic['idx'] = idx
        data_dic['project'] = i
        idx+=1
        all_data.append( data_dic )
print(len(all_data))
print(all_data[0])
vulnerable_data = []
non_vulnerable_data = []
for i in all_data:
    if i['target']==0:
        non_vulnerable_data.append(i)
    else:
        vulnerable_data.append(i)

print(len(vulnerable_data))
print(len(non_vulnerable_data))
from sklearn.utils import shuffle
shuffle_non_vulnerable_data = shuffle(non_vulnerable_data)
#shuffle_non_vulnerable_data = shuffle_non_vulnerable_data[:1983]
combine_data = shuffle_non_vulnerable_data + vulnerable_data
shuffle_combine_data = shuffle(combine_data)

from sklearn.model_selection import train_test_split

#train, test= train_test_split(shuffle_combine_data, test_size=0.2,random_state=123456)
#dev, test  = train_test_split(test, test_size=0.5)
print('______________________')
print(len(shuffle_combine_data))
#print(len(dev))
#print(len(test))
import json

for i in shuffle_combine_data:
    b = json.dumps(i)
    f2 = open('dataset-test.json', 'a')
    f2.write(b + "\n")
    f2.close()

import json

print(len(all_data))