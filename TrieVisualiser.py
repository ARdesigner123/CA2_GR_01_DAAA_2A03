import matplotlib.pyplot as plt
import networkx as nx
import scipy
import matplotlib.patches as mpatches

class TrieVisualizer:
    def __init__(self, trie):
        self.trie = trie

    def visualize_structure(self):
        print("Generating trie structure visualization (top-down with word buildup)...")

        G = nx.DiGraph()
        node_id = 0
        node_map = {}
        positions = {}
        node_colors = []

        def dfs(node, path, depth, x_offset):
            nonlocal node_id
            current_id = node_id

            # Node label is the progressive word
            label = path if path else "ROOT"
            G.add_node(current_id, label=label)
            node_map[id(node)] = current_id

            # Assign position (top-down)
            positions[current_id] = (x_offset[0], -depth)

            # Color: green if complete word, else blue
            if node.is_end_of_word:
                node_colors.append('lightgreen')
            else:
                node_colors.append('lightblue')

            node_id += 1

            for ch, child in sorted(node.children.items()):
                x_offset[0] += 1
                child_id = dfs(child, path + ch, depth + 1, x_offset)
                G.add_edge(current_id, child_id)

            return current_id

        dfs(self.trie.root, "", 0, [0])

        labels = nx.get_node_attributes(G, 'label')
        plt.figure(figsize=(14, 8))
        nx.draw(G, pos=positions, with_labels=True, labels=labels,
                node_color=node_colors, node_size=1200, font_size=10, arrows=True)

        plt.legend(handles=[
            mpatches.Patch(color='lightblue', label='Prefix'),
            mpatches.Patch(color='lightgreen', label='Complete Word')
        ])

        plt.title("Trie Structure (Progressive Word Formation)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()




    def visualize_path(self, word):
        print(f"Visualizing path for '{word}'...")

        G = nx.DiGraph()
        node = self.trie.root
        current = ""
        positions = {}
        node_colors = []

        G.add_node(current)
        positions[current] = (0, 0)
        node_colors.append('lightblue')  # root

        for i, char in enumerate(word):
            next_label = current + char
            G.add_node(next_label)
            G.add_edge(current, next_label)
            positions[next_label] = (i + 1, -i - 1)

            if char in node.children:
                node = node.children[char]
                # If this node ends a word, color it green
                if node.is_end_of_word and i == len(word) - 1:
                    node_colors.append('lightgreen')
                else:
                    node_colors.append('lightblue')
            else:
                print(f"'{word}' not found in trie.")
                return

            current = next_label

        plt.figure(figsize=(8, 5))
        nx.draw(G, pos=positions, with_labels=True, node_color=node_colors,
                node_size=1000, font_size=10, arrows=True)
        plt.title(f"Path for '{word}'")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


    def visualize_subtree_from_prefix(self, prefix):
        print(f"Visualizing subtree from prefix '{prefix}'...")

        # Step 1: Find the starting node
        node = self.trie.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                print(f"Prefix '{prefix}' not found in trie.")
                return

        # Step 2: Build graph for subtree
        G = nx.DiGraph()
        node_colors = {}
        positions = {}
        node_id_map = {}
        next_id = [0]

        def dfs(current_node, path, depth, x_offset):
            cur_id = next_id[0]
            next_id[0] += 1
            G.add_node(cur_id, label=path if path else "ROOT")
            positions[cur_id] = (x_offset[0], -depth)
            node_colors[cur_id] = 'lightgreen' if current_node.is_end_of_word else 'lightblue'

            for ch, child in sorted(current_node.children.items()):
                x_offset[0] += 1
                child_id = dfs(child, path + ch, depth + 1, x_offset)
                G.add_edge(cur_id, child_id)

            return cur_id

        dfs(node, prefix, 0, [0])

        # Step 3: Draw
        labels = nx.get_node_attributes(G, 'label')
        colors = [node_colors[n] for n in G.nodes()]
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos=positions, with_labels=True, labels=labels,
                node_color=colors, node_size=1200, font_size=10, arrows=True)

        plt.legend(handles=[
            mpatches.Patch(color='lightblue', label='Prefix'),
            mpatches.Patch(color='lightgreen', label='Complete Word')
        ])
        plt.title(f"Subtree for prefix '{prefix}'")
        plt.axis('off')
        plt.tight_layout()
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
