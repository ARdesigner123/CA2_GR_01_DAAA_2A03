class TrieIO:
    def __init__(self, trie):
        self.trie = trie

    # Save all keywords with frequencies to a file
    def save_keywords_to_file(self, filename):
        words_with_freq = self.trie.get_all_words_with_freq()
        with open(filename, 'w') as f:
            for word, freq in words_with_freq:
                f.write(f'{word},{freq}\n')

    # Load keywords from file and populate the trie
    def load_keywords_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if ',' in line:
                            word, freq_str = line.rsplit(',', 1)
                            try:
                                freq = int(freq_str)
                            except ValueError:
                                freq = 1
                            for _ in range(freq):
                                self.trie.insert(word)
            print(f"Keywords loaded from '{filename}'.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    # Save visual representation of the trie to a file (as indented ASCII-like structure)
    def save_trie_visual(self, filename):
        def _display_node(node, prefix='', depth=0):
            lines = []
            indent = '.' * depth

            # Opening bracket with prefix
            lines.append(f"{indent}[{prefix}")

            # If it's a word, print it with frequency
            if node.is_end_of_word:
                lines.append(f"{indent}{'.' * 1}>{prefix}({node.frequency})*")

            # Recurse into children
            for ch, child in sorted(node.children.items()):
                lines.extend(_display_node(child, prefix + ch, depth + 1))

            # Closing bracket
            lines.append(f"{indent}]")
            return lines

        lines = _display_node(self.trie.root)
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line + '\n')
