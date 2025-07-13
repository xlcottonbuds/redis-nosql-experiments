import redis

# Connect to local Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Write a test key
# r.set('test_key', 'test_value')

# Read the data just written
# value = r.get('test_key')
# print('Read data:', value.decode())

# Read a specific product information from Redis after import
info = r.hgetall('product:ea91e47cac68b132887d7fc1175e91c2') #uniq_id
info = {k.decode() if isinstance(k, bytes) else k: v.decode() if isinstance(v, bytes) else v for k, v in info.items()}
print(info)
