class FeatureBase:
    def __init__(self, trie):
        self.trie = trie

    def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method.")