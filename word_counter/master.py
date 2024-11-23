import os
import json
import redis
import time
from pathlib import Path
from reducer import Reducer

class Master:
    def __init__(self, input_file, chunk_size=1000):
        self.input_file = input_file
        self.chunk_size = chunk_size
        retry_count = 0
        while retry_count < 5:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'redis'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    decode_responses=True
                )
                self.redis_client.ping()
                break
            except redis.ConnectionError:
                retry_count += 1
                print(f"Waiting for Redis... attempt {retry_count}")
                time.sleep(5)
        
    def setup(self):
        """Initialize Redis and clear any existing data"""
        self.redis_client.flushall()
        self.redis_client.delete("processing_complete")
        self.redis_client.delete("completed_chunks")
        
    def split_input(self):
        """Split input file into chunks and store in Redis."""
        chunk_id = 0
        current_chunk = []
        
        print(f"Reading input file: {self.input_file}")
        try:
            with open(self.input_file, 'r') as f:
                for line in f:
                    current_chunk.append(line.strip())
                    if len(current_chunk) >= self.chunk_size:
                        self._store_chunk(chunk_id, current_chunk)
                        chunk_id += 1
                        current_chunk = []
                
                if current_chunk:
                    self._store_chunk(chunk_id, current_chunk)
                    chunk_id += 1
            
            total_chunks = chunk_id
            print(f"Split input into {total_chunks} chunks")
            return total_chunks
            
        except Exception as e:
            print(f"Error reading input file: {str(e)}")
            return 0
    
    def _store_chunk(self, chunk_id, chunk_data):
        """Store a chunk in Redis and add to pending queue."""
        try:
            chunk_key = f"chunk:{chunk_id}"
            self.redis_client.set(chunk_key, '\n'.join(chunk_data))
            self.redis_client.lpush("pending_chunks", chunk_id)
            print(f"Stored chunk {chunk_id}")
        except Exception as e:
            print(f"Error storing chunk {chunk_id}: {str(e)}")
    
    def combine_results(self, num_chunks):
        """Combine intermediate results into final output."""
        print("Waiting for all chunks to be processed...")
        
        timeout = 60  # timeout in seconds
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            completed_chunks = self.redis_client.scard("completed_chunks")
            print(f"Completed chunks: {completed_chunks}/{num_chunks}")
            
            if completed_chunks == num_chunks:
                print("All chunks processed, combining results...")
                reducer = Reducer()
                
                # Collect all intermediate results
                for chunk_id in range(num_chunks):
                    intermediate = self.redis_client.hgetall(f"intermediate:{chunk_id}")
                    print(f"Intermediate results for chunk {chunk_id}: {intermediate}")
                    for word, count in intermediate.items():
                        reducer.reduce(word, [int(count)])
                
                # Signal processing complete
                self.redis_client.set("processing_complete", "true")
                
                results = reducer.emit()
                print(f"Final results: {results}")
                return results
                
            time.sleep(1)
        
        print("Timeout waiting for chunks to complete")
        return {}

if __name__ == "__main__":
    input_file = "input/input.txt"
    output_file = "output/results.json"
    
    print("Starting MapReduce job...")
    master = Master(input_file, chunk_size=2)  # Smaller chunk size for testing
    
    # Ensure input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found!")
        exit(1)
    
    # Initialize Redis
    master.setup()
    
    # Split input and get number of chunks
    num_chunks = master.split_input()
    if num_chunks == 0:
        print("No chunks created, exiting...")
        exit(1)
    
    # Process and combine results
    final_results = master.combine_results(num_chunks)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save results
    try:
        with open(output_file, 'w') as f:
            json.dump(final_results, f, indent=2)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")
        print("Final results:", json.dumps(final_results, indent=2))