# Python MapReduce Framework with Docker

A lightweight MapReduce implementation using Python and Docker, designed for learning and experimenting with distributed computing concepts. This framework allows you to run MapReduce jobs locally using multiple Docker containers as workers, coordinated through Redis.

## 🌟 Features

- Distributed processing with multiple workers
- Redis-based coordination and data storage
- Docker containerization for easy deployment
- Configurable chunk size for data processing
- Detailed logging and error handling
- Automatic retry logic for Redis connections
- Progress monitoring for chunk processing

## 🏗️ System Requirements

- Docker
- Docker Compose
- Git
- 4GB RAM (minimum)
- 10GB disk space

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/sandole/mapreduce-example
cd python-mapreduce
```

2. Create required directories and sample input:
```bash
# Create directories
mkdir -p input output
chmod -R 777 output  # Ensure write permissions

# Create a sample input file
echo "This is a test file." > input/input.txt
echo "It contains some text for testing." >> input/input.txt
```

3. Build and run the system:
```bash
docker-compose up --build
```

## 📊 Project Structure

```
python-mapreduce/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── input/
│   └── input.txt
├── output/
│   └── results.json
└── word_counter/
    ├── __init__.py
    ├── mapper.py
    ├── reducer.py
    ├── worker.py
    └── master.py
```

## 🔧 Configuration

### Docker Compose Configuration
The system uses three services:
- Redis: For coordination and data storage
- Master: Manages job distribution and result collection
- Workers: Process data chunks in parallel

```yaml
services:
  redis:
    image: redis:latest
  master:
    build: .
    volumes:
      - ./input:/app/input:ro
      - ./output:/app/output:rw
  worker:
    deploy:
      replicas: 3  # Number of parallel workers
```

### Processing Configuration

Adjust the chunk size in `master.py` to control data distribution:
```python
master = Master(input_file, chunk_size=2)  # Smaller chunks for testing
```

## 📝 Example Output

The system generates a JSON file with word counts:
```json
{
  "this": 1,
  "is": 1,
  "a": 1,
  "test": 2,
  "file": 1,
  "it": 1,
  "contains": 1,
  "some": 1,
  "text": 1,
  "for": 1,
  "testing": 1
}
```

## 🔍 Monitoring

1. View real-time logs:
```bash
docker-compose logs -f
```

2. Monitor specific services:
```bash
docker-compose logs -f master   # Monitor master
docker-compose logs -f worker   # Monitor workers
docker-compose logs -f redis    # Monitor Redis
```

## 🐞 Troubleshooting

### Common Issues and Solutions

1. **No output generated:**
   - Check output directory permissions: `chmod -R 777 output`
   - Verify Redis connection in logs
   - Ensure input file exists and is readable

2. **Workers exit immediately:**
   - Check Redis logs for connection issues
   - Verify network connectivity between containers
   - Check for errors in worker logs

3. **Processing hangs:**
   - Check if all workers are running: `docker-compose ps`
   - Verify chunk processing progress in logs
   - Check Redis memory usage

4. **Redis connection issues:**
   - Ensure Redis is running: `docker-compose ps redis`
   - Check Redis logs for errors
   - Verify Redis port configuration

### Debug Commands

```bash
# Check container status
docker-compose ps

# Check Redis connectivity
docker-compose exec redis redis-cli ping

# View Redis data
docker-compose exec redis redis-cli keys "*"

# Restart specific service
docker-compose restart worker

# Reset entire system
docker-compose down
docker-compose up --build
```

## 🛠️ Creating Custom MapReduce Jobs

1. Extend the base Mapper class:
```python
class CustomMapper(Mapper):
    def map(self, line):
        # Custom mapping logic
        pass
```

2. Extend the base Reducer class:
```python
class CustomReducer(Reducer):
    def reduce(self, key, values):
        # Custom reduction logic
        pass
```

## 🔄 Development Workflow

1. Make code changes in the `word_counter` directory
2. Rebuild and restart the system:
```bash
docker-compose down
docker-compose up --build
```

## 📦 Production Considerations

1. **Data Persistence:**
   - Mount Redis data volume for persistence
   - Implement checkpoint mechanism for long-running jobs

2. **Scaling:**
   - Adjust worker replicas based on workload
   - Monitor Redis memory usage
   - Consider implementing worker queue management

3. **Security:**
   - Implement Redis authentication
   - Use secure networking between containers
   - Implement proper access controls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- Inspired by Google's MapReduce paper
- Built with Python, Redis, and Docker
- Community contributions welcome

For questions or issues, please open a GitHub issue in the repository