# # Copyright (c) Microsoft Corporation.
# # Licensed under the MIT License.
# import torch
# import torch.nn as nn
# import torch
# from torch.autograd import Variable
# import copy
# from torch.nn import CrossEntropyLoss, MSELoss
# from transformers import AutoTokenizer, AutoModel
import loralib as lora
# # model = AutoModel.from_pretrained("microsoft/codebert-base")
#
# class Model(nn.Module):
#     def __init__(self, encoder, config, tokenizer, args, context_embedding):
#         super(Model, self).__init__()
#         self.encoder = encoder
#         self.config = config
#         self.tokenizer = tokenizer
#         self.args = args
#     def forward(self, input_ids=None, labels=None):
#         outputs = self.encoder(input_ids, attention_mask=input_ids.ne(1))[0]
#         print(outputs.shape)
#
#         logits = outputs
#         prob = torch.sigmoid(logits)
#         if labels is not None:
#             labels = labels.float()
#             loss = torch.log(prob[:, 0] + 1e-10) * labels + torch.log((1 - prob)[:, 0] + 1e-10) * (1 - labels)
#             loss = -loss.mean()
#             return loss, prob
#         else:
#             return prob
#
#
#            (XLNET)
import numpy as np
import torch
import torch.nn as nn
import torch
from torch.autograd import Variable
import copy
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss, MSELoss
class Model(nn.Module):

    def __init__(self, encoder, config, tokenizer, args, context_embedding):
        super(Model, self).__init__()
        self.embeddimg = context_embedding
        self.args=args

        self.conv = nn.Conv1d(768,128,kernel_size=3,padding='valid')
        self.flatten = nn.Flatten()

        self.lstm_0 = nn.LSTM(128, 64,num_layers=1, bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(p=0.5)
        self.maxpool = nn.MaxPool1d(self.args.block_size - 3 + 1, stride=1)
        self.dense1 = nn.Linear(128, 64)
        self.dense2 = nn.Linear(64, 32)
        self.dense3 = nn.Linear(32, 1)

    def forward(self, input_ids=None, labels=None):
        input_ids = self.embeddimg(input_ids)[0]

        cnn= F.relu(self.conv(input_ids.permute(0,2,1)))
        input_ids_clstm ,_= self.lstm_0(cnn.permute(0,2,1))
        input_ids_clstm = torch.tanh(input_ids_clstm)
        input_ids_clstm = self.dropout(input_ids_clstm)

        input_ids_clstm = self.maxpool(input_ids_clstm.permute(0,2,1))
        input_ids_clstm = input_ids_clstm.permute(0, 2, 1)
        input_ids_clstm = input_ids_clstm.squeeze(1)
        input_ids_clstm = self.dropout(input_ids_clstm)

        input_ids = F.relu(self.dense1(input_ids_clstm ))
        input_ids = self.dense2(input_ids)
        input_ids = self.dense3(input_ids)

        prob = torch.sigmoid(input_ids)

        if labels is not None:

            labels = labels.float()
            loss = torch.log(prob[:, 0] + 1e-10) * labels + torch.log((1 - prob)[:, 0] + 1e-10) * (1 - labels)
            loss = -loss.mean()
            return loss, prob
        else:
            return prob

#
# # Copyright (c) Microsoft Corporation.
# # Licensed under the MIT License.
# import torch
# import torch.nn as nn
# import torch
# from torch.autograd import Variable
# import copy
# from torch.nn import CrossEntropyLoss, MSELoss
# from transformers import AutoTokenizer, AutoModel
# import loralib as lora
#
#
# # model = AutoModel.from_pretrained("microsoft/codebert-base")
#
# class Model(nn.Module):
#     def __init__(self, encoder, config, tokenizer, args, context_embedding):
#         super(Model, self).__init__()
#         self.encoder = encoder
#         self.config = config
#         self.tokenizer = tokenizer
#         self.args = args
#         self.model = context_embedding
#
#         self.lora_linear = nn.Linear(28996, 8)
#         # self.lora_linear_1 = lora.Linear(8, 8, r=8)
#
#         self.lora_linear_4 = nn.Linear(8, 1)
#         self.lora_linear_last = nn.Linear(1, 1)
#
#         self.lora_conv1d = nn.Conv1d(in_channels=400, out_channels=1, kernel_size=1)
#
#     def forward(self, input_ids=None, labels=None):
#
#         # print(input_ids.shape)#[4,400]
#         # outputs = self.model(torch.tensor(input_ids)[None, :])[0]
#         outputs = self.encoder(input_ids, attention_mask=input_ids.ne(1))[0]
#
#         # logits = outputs
#         # print(outputs.shape)#[1,4,400,768]
#         outputs = outputs.squeeze(0)
#         print(outputs.shape)
#         logits = self.lora_conv1d(outputs)
#         print(logits.shape)  # [4,400,8]
#         logits = self.lora_linear(logits)
#         print(logits.shape)  # [4,400,8]
#
#         logits4 = self.lora_linear_4(logits)
#         # logits4 = logits4.unsqueeze(-1)
#         # logits_conv1d = self.lora_conv1d(logits4)
#         # logits_conv1d = logits_conv1d.squeeze(-1)
#         # lora_linear.Flatten
#         # self.lora_linear.Flatten
#
#         # logits4 = logits4.view(-1)
#         print(logits4.shape)  # [4,400,1]
#
#         # logits4 = self.lora_conv1d(logits4)
#
#         # print(logits4.shape)#[4,1,1]
#         logits_last = self.lora_linear_last(logits4)
#
#         prob = torch.sigmoid(logits_last)
#         # prob = torch.sigmoid(logits_conv1d)
#
#         if labels is not None:
#             labels = labels.float()
#             # loss1=CrossEntropyLoss()
#             # loss=loss1(logits,labels)
#             loss = torch.log(prob[:, 0] + 1e-10) * labels + torch.log((1 - prob)[:, 0] + 1e-10) * (1 - labels)
#             loss = -loss.mean()
#             return loss, prob
#         else:
#             return prob
#
#
#
#
#
# # lora
#
# # Copyright (c) Microsoft Corporation.
# # Licensed under the MIT License.
# import torch
# import torch.nn as nn
# import torch
# from torch.autograd import Variable
# import copy
# from torch.nn import CrossEntropyLoss, MSELoss
# from transformers import AutoTokenizer, AutoModel
# import loralib as lora
#
#
# # model = AutoModel.from_pretrained("microsoft/codebert-base")
#
# class Model(nn.Module):
#     def __init__(self, encoder, config, tokenizer, args, context_embedding):
#         super(Model, self).__init__()
#         self.encoder = encoder
#         self.config = config
#         self.tokenizer = tokenizer
#         self.args = args
#         self.model = context_embedding
#
#         self.lora_linear = lora.Linear(768, 8, r=8)
#         # self.lora_linear_1 = lora.Linear(8, 8, r=8)
#
#         self.lora_linear_4 = lora.Linear(8, 1, r=8)
#         self.lora_linear_last = lora.Linear(1, 1, r=8)
#
#         self.lora_conv1d = lora.Conv1d(in_channels=400, out_channels=1, kernel_size=1, r=8)
#
#     def forward(self, input_ids=None, labels=None):
#
#         # print(input_ids.shape)#[4,400]
#         outputs = self.model(torch.tensor(input_ids)[None, :])[0]
#         # outputs = self.encoder(input_ids, attention_mask=input_ids.ne(1))[0]
#
#         # logits = outputs
#         # print(outputs.shape)#[1,4,400,768]
#         outputs = outputs.squeeze(0)
#         # print(outputs.shape)
#         logits = self.lora_linear(outputs)
#         # print(logits.shape) #[4,400,8]
#
#         logits4 = self.lora_linear_4(logits)
#         # logits4 = logits4.unsqueeze(-1)
#
#         # logits_conv1d = self.lora_conv1d(logits4)
#         # logits_conv1d = logits_conv1d.squeeze(-1)
#         # lora_linear.Flatten
#         # self.lora_linear.Flatten
#
#         # logits4 = logits4.view(-1)
#         # print(logits4.shape)#[4,400,1]
#         logits4 = self.lora_conv1d(logits4)
#         # print(logits4.shape)#[4,1,1]
#         logits_last = self.lora_linear_last(logits4)
#
#         prob = torch.sigmoid(logits_last)
#         # prob = torch.sigmoid(logits_conv1d)
#
#         if labels is not None:
#             labels = labels.float()
#             # loss1=CrossEntropyLoss()
#             # loss=loss1(logits,labels)
#             loss = torch.log(prob[:, 0] + 1e-10) * labels + torch.log((1 - prob)[:, 0] + 1e-10) * (1 - labels)
#             loss = -loss.mean()
#             return loss, prob
#         else:
#             return prob
