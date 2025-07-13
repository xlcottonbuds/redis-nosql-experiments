import redis
import threading
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
N = 20000      # Total number of records to write
n_threads = 500 # Number of threads to use

read_count = 0

# Function to read data in a thread
def read_worker(start, end, result_list):
    local_count = 0
    for i in range(start, end):
        key = f'concurrency_test:{i}'
        val = r.get(key)
        if val is not None:
            local_count += 1
    result_list.append(local_count)

threads = []
results = []
batch = N // n_threads
start_time = time.time()

# Create and start threads
for t in range(n_threads):
    start = t * batch
    end = (t+1) * batch if t < n_threads-1 else N
    thread = threading.Thread(target=read_worker, args=(start, end, results))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

end_time = time.time()

# Check the actual number of entries read from Redis and verify data consistency
total_read = sum(results)
print(f"Theoretically number of reads: {N}; Actual number of reads: {total_read}")
print(f"Total time taken for concurrent reads: {end_time - start_time:.3f} seconds, throughput: {N/(end_time - start_time):.1f} entries/second")
print("Data loss detected:", "No" if total_read == N else "Yes")
