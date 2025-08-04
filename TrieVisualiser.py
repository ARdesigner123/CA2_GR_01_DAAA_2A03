import matplotlib.pyplot as plt
import networkx as nx
import scipy

class TrieVisualizer:
    def __init__(self, trie):
        self.trie = trie

    def visualize_structure(self):
        print("Generating trie structure visualization with networkx...")

        G = nx.DiGraph()
        node_id = 0
        node_map = {}  # Map from id(node) to node_id

        def dfs(node, path):
            nonlocal node_id
            current_id = node_id
            label = path[-1] if path else "ROOT"
            G.add_node(current_id, label=label)
            node_map[id(node)] = current_id
            node_id += 1

            for ch, child in node.children.items():
                child_id = dfs(child, path + ch)
                G.add_edge(current_id, child_id)

            return current_id

        dfs(self.trie.root, "")

        labels = nx.get_node_attributes(G, 'label')
        pos = nx.spring_layout(G, k=0.5, iterations=100)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue',
                node_size=1200, font_size=10, arrows=True)
        plt.title("Trie Structure")
        plt.show()

    def visualize_path(self, word):
        G = nx.DiGraph()
        node = self.trie.root
        current = ''

        for char in word:
            G.add_edge(current, current + char)
            current += char
            if char in node.children:
                node = node.children[char]
            else:
                print(f"'{word}' not found in trie.")
                return

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
        plt.title(f"Path for '{word}'")
        plt.show()

    def visualize_frequencies(self):
        words = []
        freqs = []

        def dfs(node, prefix):
            if node.is_end_of_word:
                words.append(prefix)
                freqs.append(node.frequency)
            for char, child in node.children.items():
                dfs(child, prefix + char)

        dfs(self.trie.root, "")

        if not words:
            print("Trie is empty.")
            return

        plt.figure(figsize=(10, 5))
        plt.bar(words, freqs, color='skyblue')
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Keyword Frequencies in Trie")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def visualize_subtree_from_prefix(self, prefix):
        # Step 1: Navigate to the prefix node
        node = self.trie.root
        current = ""
        for char in prefix:
            if char in node.children:
                node = node.children[char]
                current += char
            else:
                print(f"Prefix '{prefix}' not found in trie.")
                return

        # Step 2: Build graph from the subtree
        G = nx.DiGraph()

        def dfs(n, path_label):
            for char, child in n.children.items():
                next_label = path_label + char
                G.add_edge(path_label, next_label)
                dfs(child, next_label)

        dfs(node, prefix)

        # Step 3: Draw
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightgreen',
                node_size=800, font_size=10, arrows=True)
        plt.title(f"Subtree from prefix '{prefix}'")
        plt.show()

    def get_longest_path(self):
        def dfs(node, path):
            nonlocal longest_path
            if node.is_end_of_word and len(path) > len(longest_path):
                longest_path = path[:]
            for char, child in node.children.items():
                path.append(char)
                dfs(child, path)
                path.pop()

        longest_path = []
        dfs(self.trie.root, [])
        return ''.join(longest_path)
