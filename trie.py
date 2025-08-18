import string

# ----------------------- Trie Node Class -----------------------
# Class created by Aaron to represent each node in the trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # Stores frequency of word appearance

# ----------------------- Trie Class -----------------------
# Class created by Aaron. Main trie implementation to support insert, delete, search, etc.
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    # Insert a word and update frequency
    def insert(self, word):
        current = self.root
        for ch in word:
            if ch not in current.children:
                current.children[ch] = TrieNode()
            current = current.children[ch]
        if current.is_end_of_word:
            current.frequency += 1  # increment if already exists
        else:
            current.is_end_of_word = True
            current.frequency = 1  # new word
    
    # Delete one occurrence of a word
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                node.frequency -= 1
                if node.frequency <= 0:
                    node.is_end_of_word = False
                    node.frequency = 0
                    return len(node.children) == 0
                return False
            
            ch = word[depth]
            if ch not in node.children:
                return False
            
            should_delete_child = _delete(node.children[ch], word, depth + 1)
            
            if should_delete_child:
                del node.children[ch]
                return not node.is_end_of_word and len(node.children) == 0
            
            return False
        
        _delete(self.root, word, 0)
    
    # Search for a word in the trie
    def search(self, word):
        current = self.root
        for ch in word:
            if ch not in current.children:
                return False
            current = current.children[ch]
        return current.is_end_of_word
    
    # Display the trie visually with indentations
    def display(self, node=None):
        if node is None:
            node = self.root
        
        def _display(current, prefix, depth):
            lines = []
            indent = '.' * depth
            
            # Print the prefix at the current level
            lines.append(indent + '[' + prefix)
            
            # If it's a word, print it with frequency
            if current.is_end_of_word:
                lines.append('.' * (depth + 1) + f">" + prefix + f"({current.frequency})*")
            
            # Recurse into children
            for ch, next_node in sorted(current.children.items()):
                lines.extend(_display(next_node, prefix + ch, depth + 1))
            
            # Closing bracket
            lines.append(indent + ']')
            return lines
        
        print("[")
        for ch, next_node in sorted(node.children.items()):
            result = _display(next_node, ch, 1)
            for line in result:
                print(line)
        print("]")
    
    # Return all words and their frequencies
    def get_all_words_with_freq(self, prefix='', frequency=True):
        # Helper: find the node of the prefix first
        def find_prefix_node(node, prefix):
            current = node
            for ch in prefix:
                if ch not in current.children:
                    return None
                current = current.children[ch]
            return current

        start_node = find_prefix_node(self.root, prefix)
        if not start_node:
            return []

        words = []

        def _dfs(current, current_prefix):
            if current.is_end_of_word:
                if frequency:
                    words.append((current_prefix, current.frequency))
                else:
                    words.append(current_prefix)
            for ch, node in current.children.items():
                _dfs(node, current_prefix + ch)

        _dfs(start_node, prefix)
        return words
    
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
                                self.insert(word)
            print(f"Keywords loaded from '{filename}'.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    # Save Keywords to File
    def save_keywords_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                all_words = self.get_all_words_with_freq()
                for word, freq in sorted(all_words):
                    f.write(f"{word},{freq}\n")
            print(f"Keywords saved to '{filename}'.")
        except Exception as e:
            print(f"Error saving to file '{filename}': {e}")
    
    # Get predictions with support for wildcards '*'
    def get_words_with_prefix(self, prefix, max_results=50):
        results = []

        def _dfs(node, current_prefix, index):
            if len(results) >= max_results:
                return

            if index == len(prefix):
                if node.is_end_of_word:
                    results.append((current_prefix, node.frequency))
                for ch, next_node in node.children.items():
                    _dfs(next_node, current_prefix + ch, index)
                return

            ch = prefix[index]
            if ch == '*':
                for next_ch, next_node in node.children.items():
                    _dfs(next_node, current_prefix + next_ch, index + 1)
                    if len(results) >= max_results:
                        return
            elif ch in node.children:
                _dfs(node.children[ch], current_prefix + ch, index + 1)

        _dfs(self.root, '', 0)
        return results

    def find_best_match(self, pattern):
        best_match = ("", -1)
        memo = {}

        def _dfs(node, index, path):
            nonlocal best_match

            key = (id(node), index)
            if key in memo and memo[key] >= best_match[1]:
                return
            memo[key] = best_match[1]

            if index == len(pattern):
                if node.is_end_of_word and node.frequency > best_match[1]:
                    best_match = (path, node.frequency)
                return

            ch = pattern[index]
            if ch == '*':
                for next_ch, child in node.children.items():
                    _dfs(child, index + 1, path + next_ch)
            elif ch in node.children:
                _dfs(node.children[ch], index + 1, path + ch)

        _dfs(self.root, 0, "")
        return best_match[0] if best_match[1] > 0 else None
    
    def separate_words(self, text):
        return text.strip().split()

    def loop_Sentence(self, array):
        result = []
        for word in array:
            # Separate trailing punctuation except '*'
            stripped_word = word.rstrip(string.punctuation.replace('*', ''))
            trailing_punct = word[len(stripped_word):]

            if '*' in word:
                restored_word = self.find_best_match(stripped_word)
                if restored_word is not None:
                    result.append(restored_word + trailing_punct)
                else:
                    result.append(word)
            else:
                result.append(word)
        return ' '.join(result)
    
    def loop_Sentence_AllMatches(self, array):
        result = []
        for word in array:
            stripped_word = word.rstrip(string.punctuation.replace('*', ''))
            trailing_punct = word[len(stripped_word):]
            stripped_word_clean = stripped_word.rstrip('*')

            if '*' in word:
                matches = self.get_all_words_with_freq(stripped_word_clean, False)
                if matches:
                    result.append('/'.join(matches) + trailing_punct)
                else:
                    result.append(word)
            else:
                result.append(word)
        return ' '.join(result)