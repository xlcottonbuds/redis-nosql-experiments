import redis
import pandas as pd
from tqdm import tqdm

# Connect to local Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Read product info
df = pd.read_csv('flipkart_com-ecommerce_sample.csv', encoding='utf-8')

# Batch write to Redis hash
for idx, row in tqdm(df.iterrows(), total=len(df)):
    uniq_id = str(row['uniq_id'])
    key = f'product:{uniq_id}'
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


print(f"Successfully imported {len(df)} items of product information into Redis!")
