import datetime
import pandas as pd
import torch
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
from itertools import chain
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from src.utils import getAccuracy
from src.model import DevignLightning
from src.prepare import JoernExeError, GraphDataLightning, DatasetBuilder
from src.utils import PROJECT_ROOT, parse_args, process_joern_error, setup, extract_representations, ListToCSV, extract_train_set_repre, extract_validation_set_repre, extract_test_set_repre, save_pickle, load_pickle
from sklearn.utils import class_weight
from sklearn.metrics import classification_report, confusion_matrix
import pickle as cPickle
print(torch.cuda.is_available())
# 1：定义用于获取网络各层输入输出tensor的容器
# 并定义module_name用于记录相应的module名字
module_name = []
features_in_hook = []
features_out_hook = []

# 2：hook函数负责将获取的输入输出添加到feature列表中
# 并提供相应的module名字
def hook(module, fea_in, fea_out):
    print("hooker working")
    module_name.append(module.__class__)
    features_in_hook.append(fea_in)
    features_out_hook.append(fea_out)
    return None

def main(args):
    # check if namespace is empty
    if not len(vars(args)):
        # setup was invoked
        setup()
        print('Setup is finished.')
        return 0
    test_build = args.scope == 'sample'
    if 'architecture' not in args:
        # prepare was invoked
        try:
            DatasetBuilder(fresh_build=True, test_build=test_build, data_path='graphs')
            return 0
        except JoernExeError:
            return process_joern_error(test_build)
    # model run was invoked
    model_kwargs = {
        'input_channels': 782,
        'hidden_channels': 800,
        'num_layers': 6
    }
    lr = 1e-4
    data_kwargs = {
        'fresh_build': args.rebuild,
        'test_build': test_build,

        'num_nodes': np.inf if args.architecture == 'flat' else 200,
        'train_proportion': 0.70,
        'batch_size': 16,

    }
    pl.seed_everything(42)
    model = DevignLightning(args.architecture, lr, **model_kwargs)
    try:
        data_module = GraphDataLightning(**data_kwargs) # Run this for the first time.
        #with open('data_module.pkl', 'wb') as module:
            #cPickle.dump(data_module, module)
        # Load the saved dataset
        """
        module = open("data_module.pkl", "rb")
        data_module = cPickle.load(module)

        data_module = GraphDataLightning(**data_kwargs)
        with open('data_module.pkl', 'wb') as module:
            cPickle.dump(data_module, module)
        """
    except JoernExeError:
        return process_joern_error(test_build)
    # Lightning training
    checkpoint_callback = ModelCheckpoint(monitor="val_loss",
                                          verbose=True,
                                          mode='min',
                                          dirpath=os.getcwd() + os.sep + "data" + os.sep + "models" + os.sep,
                                          save_top_k = 2,
                                          filename='{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}')

    trainer = pl.Trainer(gpus= 1 if torch.cuda.is_available() else 0,
                         max_epochs= 5 if data_kwargs['test_build'] else 10,

                         log_every_n_steps = 6 if data_kwargs['test_build'] else 10, callbacks=[checkpoint_callback], num_sanity_val_steps=0)


    train_dataloader = data_module.train_dataloader()
    val_dataloader = data_module.val_dataloader()
    test_dataloader = data_module.test_dataloader()


    if 'representations' not in args:
        trainer.fit(model, train_dataloader, val_dataloader)
        train_results = trainer.test(dataloaders = train_dataloader, verbose=True)
        print('length of train_y')
        print(len(data_module.train_y))
        print('length of val_y')
        print(len(data_module.validation_y))
        print('length of test_y')
        print(len(data_module.test_y))

        print('TRAIN RESULTS')
        for metric, value in train_results[0].items():
            print('  ', metric.replace('test', 'train'))
            print('    ', value)


    else:
        # Extract representations
        lg_model = model.load_from_checkpoint(
            checkpoint_path="/home/mxy/yx/liiin/Graph_represenations/data/models/epoch=01-val_loss=0.11-val_acc=0.00.ckpt")
        lg_model = lg_model.cuda()
        lg_model.eval()
        feature_arr = []

        new_trainer = pl.Trainer(gpus=1 if torch.cuda.is_available() else 0, callbacks=[checkpoint_callback])
        extract_train_set_repre(lg_model, new_trainer, data_module)
        extract_validation_set_repre(lg_model, new_trainer, data_module)
        extract_test_set_repre(lg_model, new_trainer, data_module)

    
    return 0
if __name__ == "__main__":
    args = parse_args()
    main(args)

