import os
import json
import redis
import time
from mapper import Mapper
from reducer import Reducer

class Worker:
    def __init__(self):
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
        
    def process_chunk(self, chunk_id):
        try:
            # Get chunk data from Redis
            chunk_data = self.redis_client.get(f"chunk:{chunk_id}")
            if not chunk_data:
                print(f"No data found for chunk {chunk_id}")
                return
            
            print(f"Processing chunk {chunk_id}")
            # Map phase
            mapper = Mapper()
            for line in chunk_data.split('\n'):
                mapper.map(line)
            
            # Store intermediate results
            intermediate_results = mapper.emit()
            self.redis_client.hset(
                f"intermediate:{chunk_id}",
                mapping={word: str(count) for word, count in intermediate_results}
            )
            
            # Mark this chunk as completed
            self.redis_client.sadd("completed_chunks", chunk_id)
            print(f"Completed chunk {chunk_id}")
            
        except Exception as e:
            print(f"Error processing chunk {chunk_id}: {str(e)}")
        
    def run(self):
        print("Worker starting...")
        while True:
            try:
                # Check if processing is complete
                if self.redis_client.get("processing_complete"):
                    print("Processing complete signal received")
                    break
                
                # Try to get a chunk to process
                chunk_id = self.redis_client.rpop("pending_chunks")
                if chunk_id:
                    self.process_chunk(chunk_id)
                else:
                    time.sleep(1)  # Wait before checking again
                    
            except Exception as e:
                print(f"Worker error: {str(e)}")
                time.sleep(1)
                
        print("Worker shutting down...")

if __name__ == "__main__":
    worker = Worker()
    worker.run()