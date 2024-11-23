import os
import json
import redis
from mapper import Mapper
from reducer import Reducer

class Worker:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        
    def process_chunk(self, chunk_id):
        """Process a chunk of data through map and reduce phases."""
        # Get chunk data from Redis
        chunk_data = self.redis_client.get(f"chunk:{chunk_id}")
        if not chunk_data:
            return
        
        # Map phase
        mapper = Mapper()
        for line in chunk_data.split('\n'):
            mapper.map(line)
        
        # Store intermediate results
        intermediate_results = mapper.emit()
        self.redis_client.hset(
            f"intermediate:{chunk_id}",
            mapping={word: count for word, count in intermediate_results}
        )
        
    def run(self):
        """Main worker loop."""
        while True:
            # Try to get a chunk to process
            chunk_id = self.redis_client.rpop("pending_chunks")
            if not chunk_id:
                continue
            
            self.process_chunk(chunk_id)