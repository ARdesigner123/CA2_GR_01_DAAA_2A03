import matplotlib.pyplot as plt
from user_interface import UserInterface as UI
from trie_editor import Trie, TrieEditor,TrieNode

class TrieChart:
    def __init__(self, trie):
        self.trie = trie

    def _plot_bar_chart(self, title, data, xlabel, ylabel):
        labels = list(data.keys())
        values = list(data.values())
        plt.figure(figsize=(10, 5))
        plt.bar(labels, values, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def _chart_by_first_letter(self):
        print("Generating chart by first letter...")
        letter_counts = {}

        def dfs(node, path):
            if node.is_end_of_word and path:
                letter_counts[path[0]] += 1
            for ch in node.children:
                dfs(node.children[ch], path + ch)

        dfs(self.trie.root, "")
        self._plot_bar_chart("Words by Starting Letter", letter_counts, "First Letter", "Word Count")

    def _chart_by_word_length(self):
        print("Generating chart by word length...")
        length_data = self.trie.get_word_length_histogram()
        self._plot_bar_chart("Words by Length", length_data, "Word Length", "Frequency")

    def _chart_by_frequency(self):
        print("Generating chart by frequency...")
        top_words = self.trie.get_top_n_frequent_words(20)
        word_freqs = {word: freq for word, freq in top_words}
        self._plot_bar_chart("Top 20 Frequent Words", word_freqs, "Word", "Frequency")
