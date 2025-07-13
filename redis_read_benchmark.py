import redis
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

# Connect to local Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# Read product info
df = pd.read_csv('flipkart_com-ecommerce_sample.csv', encoding='utf-8')
# Define batch sizes and number of rounds
sizes = [100, 500, 1000, 5000, 10000, 15000, 20000]
n_rounds = 5 

read_times_avg = []
read_times_std = []
read_throughputs_avg = []
read_throughputs_std = []

for size in sizes:
    times = []
    throughputs = []
    for rnd in range(n_rounds):
        start = time.time()
        for idx in range(size):
            uniq_id = str(df.iloc[idx]['uniq_id'])
            key = f'product_test:{uniq_id}'
            _ = r.hgetall(key)
        end = time.time()
        total_time = end - start
        throughput = size / total_time if total_time > 0 else 0
        times.append(total_time)
        throughputs.append(throughput)
        print(f'[Round {rnd+1}] Reading {size} records takes: {total_time:.3f}s, throughput: {throughput:.1f} records/second')
    read_times_avg.append(np.mean(times))
    read_times_std.append(np.std(times))
    read_throughputs_avg.append(np.mean(throughputs))
    read_throughputs_std.append(np.std(throughputs))
    print(f'>>> Batch size {size}: Average time {np.mean(times):.3f}s (±{np.std(times):.3f}), Average throughput {np.mean(throughputs):.1f} (±{np.std(throughputs):.1f})')

# Visualize the results
# Total read time
plt.figure(figsize=(8,4))
plt.errorbar(sizes, read_times_avg, yerr=read_times_std, marker='o', color='tab:blue', capsize=4)
plt.title('Redis Batch Read Total Time (mean ± std)')
plt.xlabel('Number of Records')
plt.ylabel('Total Time (seconds)')
plt.grid(True)
plt.tight_layout()
plt.savefig('redis_read_time_avg.png')
plt.show()
# Throughput
plt.figure(figsize=(8,4))
plt.errorbar(sizes, read_throughputs_avg, yerr=read_throughputs_std, marker='s', color='tab:orange', capsize=4)
plt.title('Redis Batch Read Throughput (mean ± std)')
plt.xlabel('Number of Records')
plt.ylabel('Throughput (records/second)')
plt.grid(True)
plt.tight_layout()
plt.savefig('redis_read_throughput_avg.png')
plt.show()
