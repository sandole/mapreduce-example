from collections import defaultdict

class Mapper:
    def __init__(self):
        self.word_counts = defaultdict(int)
    
    def map(self, line):
        """Map function that counts words in a line."""
        words = line.strip().lower().split()
        for word in words:
            word = ''.join(c for c in word if c.isalnum())
            if word:
                self.word_counts[word] += 1
    
    def emit(self):
        """Emit intermediate key-value pairs."""
        return [(word, count) for word, count in self.word_counts.items()]