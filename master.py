import os
import redis
from pathlib import Path

class Master:
    def __init__(self, input_file, chunk_size=1000):
        self.input_file = input_file
        self.chunk_size = chunk_size
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        
    def split_input(self):
        """Split input file into chunks and store in Redis."""
        chunk_id = 0
        current_chunk = []
        
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
        
        return chunk_id
    
    def _store_chunk(self, chunk_id, chunk_data):
        """Store a chunk in Redis and add to pending queue."""
        chunk_key = f"chunk:{chunk_id}"
        self.redis_client.set(chunk_key, '\n'.join(chunk_data))
        self.redis_client.lpush("pending_chunks", chunk_id)
    
    def combine_results(self, num_chunks):
        """Combine intermediate results into final output."""
        reducer = Reducer()
        
        # Collect all intermediate results
        for chunk_id in range(num_chunks):
            intermediate = self.redis_client.hgetall(f"intermediate:{chunk_id}")
            for word, count in intermediate.items():
                reducer.reduce(word, [int(count)])
        
        return reducer.emit()

if __name__ == "__main__":
    master = Master("input.txt")
    num_chunks = master.split_input()
    # Wait for workers to process chunks
    # Combine results
    final_results = master.combine_results(num_chunks)
    print(json.dumps(final_results, indent=2))