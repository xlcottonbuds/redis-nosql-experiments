import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
count = 0
for key in r.scan_iter("persistence_test:*"):
    count += 1
print(f"Number of related products in persistence_test:* in current Redis: {count}")
