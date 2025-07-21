# ----------------------------------------
# feature_base.py
# Base class for all extra features
# Done By Aaron
# ----------------------------------------

class FeatureBase:
    def __init__(self, trie):
        # Store a reference to the Trie instance
        self.trie = trie

    def run(self):
        # Subclasses must override this method
        raise NotImplementedError("Subclasses must implement the 'run' method.")