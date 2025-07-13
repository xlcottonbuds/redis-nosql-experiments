import redis
import pandas as pd
import time  

N = 10000

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
df = pd.read_csv('flipkart_com-ecommerce_sample.csv', encoding='utf-8')

start = time.time() 

for idx in range(N):
    row = df.iloc[idx]
    uniq_id = str(row['uniq_id'])
    key = f'persistence_test:{uniq_id}' 
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
throughput = N / total_time if total_time > 0 else 0

print(f"Successfully imported {N} items of product information into Redis!")
print(f"Total write time: {total_time:.3f} seconds")
print(f"Throughput: {throughput:.1f} records/second")
