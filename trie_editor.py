import os
import re
import string
from user_interface import UserInterface
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx

UI = UserInterface()

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
    
    def get_top_n_frequent_words(self, n):
        result = []
        node_visits = 0

        def dfs(node, path):
            nonlocal node_visits
            node_visits += 1
            if node.is_end_of_word:
                result.append(("".join(path), node.frequency))
            for ch in node.children:
                dfs(node.children[ch], path + [ch])
        dfs(self.root, [])
        result.sort(key=lambda x: (-x[1], x[0]))
        return result[:n], node_visits  # Return results and node visits

    def get_n_longest_words(self, n):
        result = []
        node_visits = 0

        def dfs(node, path):
            nonlocal node_visits
            node_visits += 1
            if node.is_end_of_word:
                result.append(("".join(path), len(path)))
            for ch in node.children:
                dfs(node.children[ch], path + [ch])
        dfs(self.root, [])
        result.sort(key=lambda x: (-x[1], x[0]))
        return result[:n], node_visits  # Return results and node visits

    def get_word_length_histogram(self):
        from collections import defaultdict
        length_hist = defaultdict(int)
        node_visits = 0

        def dfs(node, depth):
            nonlocal node_visits
            node_visits += 1
            if node.is_end_of_word:
                length_hist[depth] += 1
            for ch in node.children:
                dfs(node.children[ch], depth + 1)
        dfs(self.root, 0)
        return dict(sorted(length_hist.items())), node_visits  # Return histogram and node visits
    
    def _visualize_trie_structure(self):
        print("Generating trie structure visualization with networkx...")

        G = nx.DiGraph()
        node_id = 0
        node_map = {}  # Map (id(path)) → node id in networkx

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
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', node_size=1200, font_size=10, arrows=True)
        plt.title("Trie Structure")
        plt.show()

    def get_words_with_substring(self, substring):
        matches = {}

        def dfs(node, path):
            if node.is_end_of_word:
                word = path
                if substring in word:
                    matches[word] = node.frequency
            for ch, child in node.children.items():
                dfs(child, path + ch)

        dfs(self.root, "")
        return matches
    
    # Save all keywords with frequencies to a file
    def save_keywords_to_file(self, filename):
        words_with_freq = self.get_all_words_with_freq()
        with open(filename, 'w') as f:
            for word, freq in words_with_freq:
                f.write(f'{word},{freq}\n')
    
    # Save visual representation of the trie to file
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
        
        lines = _display_node(self.root)
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line + '\n')
    
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
    
    # Get predictions with support for wildcards '*'
    def get_words_with_prefix(self, prefix):
        results = []

        def _dfs(node, current_prefix, index):
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
            elif ch in node.children:
                _dfs(node.children[ch], current_prefix + ch, index + 1)

        _dfs(self.root, '', 0)
        return results
    
    def find_best_match(self, pattern):
        best_match = ("", -1)  # (word, frequency)

        def _dfs(node, index, path):
            nonlocal best_match

            if index == len(pattern):
                if node.is_end_of_word:
                    if node.frequency > best_match[1]:
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






        



# ----------------------- Trie Editor Class -----------------------
# This class handles command-line interactions for the user. Class Created By Aaron
class TrieEditor:
    #Done By Aaron
    def __init__(self):
        self.trie = Trie()
    
    # Validate file name Done By Aaron
    def is_valid_filename(self, filename):
        invalid_chars = set('<>:"/\\|?*')
        return filename and not any(char in invalid_chars for char in filename)
    
    def load_trie_from_folder(self):
        path = UI.get_trie_folder_and_file()
        if path:
            self.trie = Trie()  # Reset current trie
            self.trie.load_keywords_from_file(path)
            print("Trie loaded from selected file.")
        else:
            print("No file selected.")
    
    # Handle command input parsing Done By Aaron
    def get_input(self):
        print("> ", end='')  # Prompt with "> "
        user_input = input().strip()

        if not user_input:
            return '', ''  # return empty cmd and arg

        command_parts = user_input.split(maxsplit=1)
        cmd = command_parts[0][0] if command_parts[0] else ''
        arg = command_parts[0][1:] if len(command_parts[0]) > 1 else ''
        if len(command_parts) > 1:
            arg += ' ' + command_parts[1]

        return cmd, arg
    
    # # Graceful exit Done By Aaron
    def terminate(self):
        print("Exiting the Full Command Prompt . Bye...\n")
        print("Press enter key, to continue...")
        input()
    
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
        letter_counts = Counter()

        def dfs(node, path):
            if node.is_end_of_word and path:
                letter_counts[path[0]] += 1
            for ch in node.children:
                dfs(node.children[ch], path + ch)

        dfs(self.trie.root, "")
        self._plot_bar_chart("Words by Starting Letter", letter_counts, "First Letter", "Word Count")

    def _chart_by_word_length(self):
        print("Generating chart by word length...")
        length_data, _ = self.trie.get_word_length_histogram()
        self._plot_bar_chart("Words by Length", length_data, "Word Length", "Frequency")

    def _chart_by_frequency(self):
        print("Generating chart by frequency...")
        top_words, _ = self.trie.get_top_n_frequent_words(20)
        word_freqs = {word: freq for word, freq in top_words}
        self._plot_bar_chart("Top 20 Frequent Words", word_freqs, "Word", "Frequency")

    def _visualize_trie_structure(self):
        print("Visualizing trie structure...")

        G = nx.DiGraph()
        pos = {}  # Positions of nodes for plotting
        x_offset = [0]  # Mutable x position tracker

        def dfs(node, label, depth):
            current_label = label
            pos[current_label] = (x_offset[0], -depth)  # Position: (x, -y)
            x_offset[0] += 1  # Move right for next sibling

            for char, child in node.children.items():
                child_label = label + char
                G.add_edge(current_label, child_label)
                dfs(child, child_label, depth + 1)

        dfs(self.trie.root, "", 0)

        plt.figure(figsize=(14, 8))
        nx.draw(
            G, pos,
            with_labels=True,
            node_size=1200,
            node_color="lightblue",
            font_size=9,
            arrows=True
        )
        plt.title("Trie Structure (Letter Inheritance Tree)")
        plt.axis('off')
        plt.show()

    def _autoComplete_recursive(self, prefix, guesses):
        suggestions = self.trie.get_words_with_prefix(prefix)
        if not suggestions:
            print("No more suggestions. Ending round.")
            return guesses

        # Take up to 3 suggestions to show
        current_guesses = suggestions[:3]
        UI.Game_UI(current_guesses)

        # Ask user if any guess is correct
        user_input = input("Is the word one of these? Enter number (1-3), or 'n' for none: ").strip().lower()
        if user_input in ['1', '2', '3']:
            chosen_index = int(user_input) - 1
            chosen_word = current_guesses[chosen_index]
            print(f"Great! The word is '{chosen_word}'.")
            guesses.append(chosen_word)
            return guesses
        elif user_input == 'n':
            # User says none matched, ask for next prefix to narrow down
            new_prefix = input("Enter more letters to refine your guess (or just press Enter to stop): ").strip().lower()
            if not new_prefix:
                print("Stopping round.")
                return guesses
            return self._autoComplete_recursive(prefix + new_prefix, guesses)
        else:
            print("Invalid input, try again.")
            return self._autoComplete_recursive(prefix, guesses)

    def _start_autoComplete_round(self):
        if not hasattr(self, 'recent_rounds'):
            self.recent_rounds = []

        query = input("Enter initial prefix to start autocomplete: ").strip()
        if not query:
            print("Empty input. Try again.")
            return

        guesses = self._autoComplete_recursive(query, [])

        if guesses:
            print("Round completed! Your guesses were:", guesses)
        else:
            print("No guesses were made this round.")

        self.recent_rounds.append((query, guesses))


    def _review_recent_rounds(self):
            if not hasattr(self, 'recent_rounds'):
                self.recent_rounds = []

            if not self.recent_rounds:
                print("No recent rounds to review.")
                return

            print("Recent Rounds:")
            for i, (query, guesses) in enumerate(self.recent_rounds[-5:], 1):
                print(f"Round {i}: Query = '{query}'")
                for rank, guess in enumerate(guesses, 1):
                    print(f"   {rank}: {guess}")
                print("-" * 50)


    # Handle command prompt logic for construct_edit and predict_restore Done By Aaron
    def command_prompt(self, function, repeat=False):
        if function == "construct_edit":
            if not repeat:
                self.trie = Trie()
                UI.construct_edit(show_empty_trie=True)
            else:
                UI.construct_edit(show_empty_trie=False)
            while True:
                cmd, arg = self.get_input()
                if not cmd:
                    continue
                    
                if cmd == '+':
                    if arg.isalpha():
                        self.trie.insert(arg)
                        print(f"Added '{arg}' to trie.")
                    elif arg:
                        print("Invalid input! Please make sure the word contains letters only, no symbols.")
                    else:
                        print("Please provide a word to add.")
                elif cmd == '-':
                    if arg.isalpha():
                        if self.trie.search(arg):
                            self.trie.delete(arg)
                            print(f"Deleted '{arg}' from trie.")
                        else:
                            print("Is not a keyword in trie.")
                    elif arg:
                        print("Invalid input! Please make sure the word contains letters only, no symbols.")
                    else:
                        print("Please provide a word to delete.")
                elif cmd == '?':
                    if arg.isalpha():
                        found = self.trie.search(arg)
                        if found:
                            print(f'Keyword "{arg}" is present.')
                        else:
                            print(f'Keyword "{arg}" is not present.')
                    elif arg:
                        print("Invalid input! Please make sure the word contains letters only, no symbols.")
                    else:
                        print("Please provide a word to search.")
                elif cmd == '@':
                    print("Please enter new filename: ", end='')
                    filename = input().strip()
                    if filename:
                        self.trie.save_trie_visual(filename)
                        print(f"Trie saved to '{filename}'.")
                    else:
                        print("No filename entered.")
                elif cmd == '~':
                    print("Please enter input file: ", end='')
                    filename = input().strip()
                    if filename:
                        self.trie = Trie()  # Reset trie before loading new file
                        self.trie.load_keywords_from_file(filename)
                    else:
                        print("No filename entered.")
                elif cmd == '=':
                    if arg:
                        if self.is_valid_filename(arg):
                            try:
                                self.trie.save_keywords_to_file(arg)
                                print(f"All keywords with frequencies written to '{arg}'.")
                            except OSError:
                                print(f"Error: Cannot write to '{arg}'. Please use a valid filename.")
                        else:
                            print("Invalid filename! Please avoid special characters like \\ / : * ? \" < > |")
                    else:
                        print("Please enter new filename: ", end='')
                        filename = input().strip()
                        if filename:
                            if self.is_valid_filename(filename):
                                try:
                                    self.trie.save_keywords_to_file(filename)
                                    print(f"All keywords with frequencies written to '{filename}'.")
                                except OSError:
                                    print(f"Error: Cannot write to '{filename}'. Please use a valid filename.")
                            else:
                                print("Invalid filename! Please avoid special characters like \\ / : * ? \" < > |")
                        else:
                            print("No filename entered.")
                elif cmd == '#':
                    self.trie.display()
                elif cmd == '!':
                    UI.construct_edit(show_empty_trie=False)
                    continue
                elif cmd == '\\':
                    self.terminate()
                    return
                else:
                    print("Invalid command! Please try again.")
        #Done By Stephen
        elif function == "predict_restore":
                UI.predict_restore()
                while True:
                    cmd, arg = self.get_input()
                    if not cmd:
                        continue

                    if cmd == '~':
                        print("Please enter input file: ", end='')
                        filename = input().strip()
                        if filename:
                            self.trie.load_keywords_from_file(filename)
                        else:
                            print("No filename entered.")
                    elif cmd == '#':
                        self.trie.display()
                    elif cmd == '$':
                        print("Please enter input word: ", end='')
                        arg = input().strip()
                        print(', '.join(f"{word} ({freq})" for word, freq in self.trie.get_words_with_prefix(arg)))
                    elif cmd == '?':
                        print("Please enter input word: ", end='')
                        arg = input().strip()
                        if arg:
                            result = self.trie.find_best_match(arg)
                            if result:
                                print(f'Restored word: {result}')
                            else:
                                print("No matching word found.")
                        else:
                            print("Please provide a pattern to match.")

                    elif cmd == '&':
                        print("Please enter input text or sentence: ", end='')
                        arg = input().strip()
                        word_array = self.trie.separate_words(arg)
                        print(self.trie.loop_Sentence_AllMatches(word_array))
                    elif cmd == '@':
                        print("Please enter input text or sentence: ", end='')
                        arg = input().strip()
                        word_array = self.trie.separate_words(arg)
                        print(self.trie.loop_Sentence(word_array))
                    elif cmd == '!':
                        self.command_prompt("predict_restore")
                        return
                    elif cmd == '\\':
                        self.terminate()
                        return
                    else:
                        print("Invalid command! Please try again.")

        elif function == "trieChart":
            UI.getTrieChart()
            while True:
                cmd = input("Chart Command: ").strip()

                if cmd == '~':
                    print("Please enter input file: ", end='')
                    filename = input().strip()
                    if filename:
                        self.trie.load_keywords_from_file(filename)
                    else:
                        print("No filename entered.")
                elif cmd == '^':
                    self._chart_by_first_letter()

                elif cmd == '!':
                    self._chart_by_word_length()

                elif cmd == '%':
                    self._chart_by_frequency()

                elif cmd == '*':
                    self._visualize_trie_structure()

                elif cmd == '\\':
                    print("Exiting Trie Chart Drawing.")
                    break

                else:
                    print("Invalid command.")
        
        elif function == "autoComplete":
                UI.autoCompleteGame()
                while True:
                    cmd = input("Game Command: ").strip()
                    if cmd == '~':
                        print("Please enter input file: ", end='')
                        filename = input().strip()
                        if filename:
                            self.trie.load_keywords_from_file(filename)
                        else:
                            print("No filename entered.")
                    elif cmd == '#':
                        self.trie.display()
                    elif cmd == '1':
                        self._start_autoComplete_round()
                    elif cmd == '2':
                        self._review_recent_rounds()
                    elif cmd == '\\':
                        print("Exiting Auto Complete Game.")
                        break
                    else:
                        print("Invalid Command.")

            
                        