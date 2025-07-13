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

write_times_avg = []
write_times_std = []
write_throughputs_avg = []
write_throughputs_std = []

for size in sizes:
    times = []
    throughputs = []
    for rnd in range(n_rounds):
        # Eliminate old data interference
        for idx in range(size):
            uniq_id = str(df.iloc[idx]['uniq_id'])
            r.delete(f'product_test:{uniq_id}')
        # Write test
        start = time.time()
        for idx in range(size):
            row = df.iloc[idx]
            uniq_id = str(row['uniq_id'])
            key = f'product_test:{uniq_id}'
            product_info = {
                'crawl_timestamp': str(row.get('crawl_timestamp', '')),
                'product_url': str(row.get('product_url', '')),
                'product_name': str(row.get('product_name', '')),
                'product_category_tree': str(row.get('product_category_tree', '')),
                'pid': str(row.get('pid', '')),
                'retail_price': str(row.get('retail_price', '')),
                'discounted_price': str(row.get('discounted_price', '')),
                'image': str(row.get('image', '')),
                'is_FK_Advantage_product': str(row.get('is_FK_Advantage_product', '')),
                'description': str(row.get('description', '')),
                'product_rating': str(row.get('product_rating', '')),
                'overall_rating': str(row.get('overall_rating', '')),
                'brand': str(row.get('brand', '')),
                'product_specifications': str(row.get('product_specifications', ''))
            }
            for field, value in product_info.items():
                r.hset(key, field, value)
        end = time.time()
        total_time = end - start
        throughput = size / total_time if total_time > 0 else 0
        times.append(total_time)
        throughputs.append(throughput)
        print(f'[Round {rnd+1}] Writing {size} records takes: {total_time:.3f}s, throughput: {throughput:.1f} records/second')
    # Calculate average and std deviation
    write_times_avg.append(np.mean(times))
    write_times_std.append(np.std(times))
    write_throughputs_avg.append(np.mean(throughputs))
    write_throughputs_std.append(np.std(throughputs))
    print(f'>>> Batch size {size}: Average time {np.mean(times):.3f}s (±{np.std(times):.3f}), Average throughput {np.mean(throughputs):.1f} (±{np.std(throughputs):.1f})')

# Visualize the results
# Total write time
plt.figure(figsize=(8,4))
plt.errorbar(sizes, write_times_avg, yerr=write_times_std, marker='o', color='tab:blue', capsize=4)
plt.title('Redis Batch Write Total Time (mean ± std)')
plt.xlabel('Number of Records')
plt.ylabel('Total Time (seconds)')
plt.grid(True)
plt.tight_layout()
plt.savefig('redis_write_time_avg.png')
plt.show()
# Throughput
plt.figure(figsize=(8,4))
plt.errorbar(sizes, write_throughputs_avg, yerr=write_throughputs_std, marker='s', color='tab:orange', capsize=4)
plt.title('Redis Batch Write Throughput (mean ± std)')
plt.xlabel('Number of Records')
plt.ylabel('Throughput (records/second)')
plt.grid(True)
plt.tight_layout()
plt.savefig('redis_write_throughput_avg.png')
plt.show()
