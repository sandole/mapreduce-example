Python MapReduce Framework with Docker
A lightweight MapReduce implementation using Python and Docker, designed for learning and experimenting with distributed computing concepts. This framework allows you to run MapReduce jobs locally using multiple Docker containers as workers, coordinated through Redis.
🌟 Features

Distributed processing with multiple workers
Redis-based coordination and data storage
Docker containerization for easy deployment
Scalable worker configuration
Example word count implementation
Extensible for custom MapReduce tasks

🏗️ Architecture
The system consists of three main components:

Master Node

Splits input data into chunks
Distributes work to workers
Coordinates the final result combination


Worker Nodes

Execute map and reduce tasks
Process data chunks independently
Scale horizontally for increased performance


Redis

Coordinates between master and workers
Stores data chunks and intermediate results
Manages the work queue



📋 Prerequisites

Docker
Docker Compose
Python 3.9 or higher (for local development)
Git

🚀 Getting Started

Clone the repository:

bashCopygit clone <repository-url>
cd python-mapreduce

Create input and output directories:

bashCopymkdir input output

Add some input data:

bashCopyecho "This is a sample text file for testing MapReduce." > input/input.txt
echo "Add more text files as needed for processing." > input/input2.txt

Build and start the containers:

bashCopydocker-compose up --build
📊 Project Structure
Copypython-mapreduce/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── word_counter/
    ├── __init__.py
    ├── mapper.py
    ├── reducer.py
    ├── worker.py
    └── master.py
🔧 Configuration
Scaling Workers
Modify the docker-compose.yml file to adjust the number of workers:
yamlCopyworker:
  deploy:
    replicas: 3  # Change this number to scale workers
Chunk Size
Adjust the chunk size in master.py:
pythonCopymaster = Master("input.txt", chunk_size=1000)  # Modify chunk_size as needed
🎯 Example: Word Count
The default implementation includes a word count example. Here's how it works:

Map Phase

Input text is split into words
Each word occurrence is counted
Intermediate results are stored in Redis


Reduce Phase

Word counts from all chunks are combined
Final totals are calculated
Results are saved to output



🛠️ Creating Custom MapReduce Jobs

Create a new mapper by extending the base Mapper class:

pythonCopyclass CustomMapper(Mapper):
    def map(self, line):
        # Implement your mapping logic
        pass

Create a new reducer by extending the base Reducer class:

pythonCopyclass CustomReducer(Reducer):
    def reduce(self, key, values):
        # Implement your reduction logic
        pass
📝 Example Output
Word count results will look like this:
jsonCopy{
  "this": 1,
  "is": 1,
  "a": 1,
  "sample": 1,
  "text": 2,
  "file": 2,
  "for": 1,
  "testing": 1,
  "mapreduce": 1
}
🔍 Monitoring
Monitor your MapReduce job:

Check worker logs:

bashCopydocker-compose logs -f worker

Check Redis status:

bashCopydocker exec -it python-mapreduce_redis_1 redis-cli
🐞 Troubleshooting
Common issues and solutions:

Workers not processing data:

Check Redis connection
Verify input file permissions
Review worker logs


Slow processing:

Increase number of workers
Adjust chunk size
Monitor Redis memory usage



🤝 Contributing

Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
✨ Advanced Usage
Custom Input Formats
Modify the master's split_input method to handle different input formats:
pythonCopydef split_input(self):
    # Implement custom input parsing
    pass
Custom Output Formats
Modify the master's combine_results method to format output differently:
pythonCopydef combine_results(self):
    # Implement custom output formatting
    pass
Performance Optimization

Memory Management:

Adjust chunk sizes based on data characteristics
Implement batch processing in workers
Use Redis pipeline operations


Processing Speed:

Implement data preprocessing
Use efficient data structures
Optimize map/reduce functions



🎓 Learning Resources
To learn more about MapReduce:

Read the original MapReduce paper by Google
Experiment with different types of problems:

Text processing
Log analysis
Data aggregation
Graph processing



🚧 Future Improvements

Add support for multiple input formats
Implement fault tolerance
Add progress monitoring
Create a web interface for job management
Add support for custom partitioning strategies

For questions or issues, please open a GitHub issue in the repository.