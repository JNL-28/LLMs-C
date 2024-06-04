# LLMs-C
This project explores the performance of various large language models for vulnerability detection.

## Task Definition
This project was modified based on CodeXGLUE-main to fit our research needs. Given a source code, the task is to identify whether it is an insecure code that may attack software systems,We treat the task as binary classification (0/1), where 1 stands for insecure code and 0 for secure code.

## Dataset
We use 12 open source datasets containing Xen, VLC, samba, qemu, Pidgin, OpenSSL, LibTIFF, LibPNG, ImageMagick, Httpd, FFmpeg, Asterisk. We combine all projects and split 80%/10%/10% for training/dev/test.
After preprocessing dataset, you can obtain three .jsonl files, i.e. train.jsonl, valid.jsonl, test.jsonl
