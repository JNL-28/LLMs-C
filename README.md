# LLMs-C
This project explores the performance of various large language models for vulnerability detection.(If you have any questions, please contact 1710234003@qq.com)

## Task Definition
This project was modified based on CodeXGLUE-main to fit our research needs. Given a source code, the task is to identify whether it is an insecure code that may attack software systems,We treat the task as binary classification (0/1), where 1 stands for insecure code and 0 for secure code.

## Dataset
We use 12 open source datasets containing Xen, VLC, samba, qemu, Pidgin, OpenSSL, LibTIFF, LibPNG, ImageMagick, Httpd, FFmpeg, Asterisk. We combine all projects and split 80%/10%/10% for training/dev/test.
After preprocessing dataset(We use the Intelligent-software-vulnerability-detection-main file to process the dataset), you can obtain three .jsonl files, i.e. train.jsonl, valid.jsonl, test.jsonl

## Model
Regarding the model, we can download it from hugging face and put it under the main LLMs-C file.

## Experiments
Once we have the model and have processed the dataset to completion, experiments can be conducted. Here is a demonstration of some of the commands (for reference use).

### Fine-tune
```shell
cd code
python run.py \
    --output_dir=./saved_models \
    --model_type=roberta \
    --tokenizer_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --do_train \
    --train_data_file=../dataset/train.jsonl \
    --eval_data_file=../dataset/valid.jsonl \
    --test_data_file=../dataset/test.jsonl \
    --epoch 5 \
    --block_size 400 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456 
```

### Inference

```shell
cd code
python run.py \
    --output_dir=./saved_models \
    --model_type=roberta \
    --tokenizer_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --do_eval \
    --do_test \
    --train_data_file=../dataset/train.jsonl \
    --eval_data_file=../dataset/valid.jsonl \
    --test_data_file=../dataset/test.jsonl \
    --epoch 5 \
    --block_size 400 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate 2e-5 \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456
```
