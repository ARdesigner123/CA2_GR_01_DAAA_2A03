from feature_base import FeatureBase
import os

class WildcardSearchFeature(FeatureBase):
    def __init__(self, trie_class):
        self.trie_class = trie_class  # Accept class, not instance
        self.trie = self.trie_class()  # Create new instance

    def run(self):
        filename = input("Enter filename containing saved keywords: ").strip()

        if not filename or not os.path.isfile(filename):
            print(f"File '{filename}' not found.")
            return

        self.trie.load_keywords_from_file(filename)

        print("Trie successfully loaded from file.")
        print("\nEnter a search pattern using '*' as wildcard (e.g., c*t, *at, c**e): ")
        pattern = input("Pattern: ").strip().lower()

        if not pattern:
            print("Pattern cannot be empty.")
            return

        matches = []
        self._search_with_wildcard(self.trie.root, pattern, 0, "", matches)

        if matches:
            print(f"\nMatches for pattern '{pattern}':")
            for word in matches:
                print(" -", word)
        else:
            print(f"No matches found for pattern '{pattern}'.")

    def _search_with_wildcard(self, node, pattern, index, current_word, results):
        if index == len(pattern):
            if node.is_end_of_word:
                results.append(current_word)
            return

        char = pattern[index]

        if char == '*':
            for ch, child in node.children.items():
                self._search_with_wildcard(child, pattern, index + 1, current_word + ch, results)
        else:
            if char in node.children:
                self._search_with_wildcard(node.children[char], pattern, index + 1, current_word + char, results)