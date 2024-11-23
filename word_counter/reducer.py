from collections import defaultdict

class Reducer:
    def __init__(self):
        self.word_counts = defaultdict(int)
    
    def reduce(self, word, counts):
        """Reduce function that sums counts for each word."""
        self.word_counts[word] = sum(counts)
    
    def emit(self):
        """Emit final results."""
        return dict(self.word_counts)