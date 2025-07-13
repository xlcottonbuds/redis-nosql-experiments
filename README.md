# Redis NoSQL Experiments

This repository contains scripts and data for benchmarking Redis as a NoSQL database, including performance, persistence, and concurrency tests for a master's project.

## Contents

- `test_redis.py`, `test_import_products.py`: Test Redis status
- `redis_read_benchmark.py`, `redis_write_benchmark.py`: Read/write performance testing
- `persist_write.py`, `persist_check.py`: Persistence mechanism testing
- `threads_read.py`, `threads_write.py`: Concurrency consistency testing
- `/pic`: Some experiment result plots

## How to Run

1. Install requirements:  
   `pip install redis pandas tqdm matplotlib numpy`
2. Start local Redis server (Modify the redis.windows.conf file according to the experimental requirements)
3. Run scripts as needed for each experiment

## Dataset

- [Flipkart Product Dataset on Kaggle](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products)
