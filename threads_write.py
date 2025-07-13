import redis
import threading
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
N = 20000        # Total number of records to write
n_threads = 500  # Number of threads to use

# Clear any existing data
for key in r.scan_iter("concurrency_test:*"):
    r.delete(key)

# Function to write data in a thread
def write_worker(start, end):
    for i in range(start, end):
        key = f'concurrency_test:{i}'
        value = f'value_{i}'
        r.set(key, value)

threads = []
batch = N // n_threads
start_time = time.time()

# Create and start threads
for t in range(n_threads):
    start = t * batch
    end = (t+1) * batch if t < n_threads-1 else N
    thread = threading.Thread(target=write_worker, args=(start, end))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

end_time = time.time()

# Check the actual number of entries written to Redis and verify data consistency
actual = sum(1 for _ in r.scan_iter("concurrency_test:*"))
print(f"Theoretical number of entries: {N}; Actual number of entries in Redis: {actual}")
print(f"Total time taken for concurrent writes: {end_time - start_time:.3f} seconds, throughput: {N/(end_time - start_time):.1f} entries/second")
print("Data loss detected:", "No" if actual == N else "Yes")
