import os
from user_interface import UserInterface

UI = UserInterface()

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # NEW: to store frequency count

class Trie:
    def __init__(self):
        self.root = TrieNode()

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

    def delete(self, word):
        def _delete(current, word, index):
            if index == len(word):
                if not current.is_end_of_word:
                    return False
                current.is_end_of_word = False
                return len(current.children) == 0
            ch = word[index]
            if ch not in current.children:
                return False
            should_delete_child = _delete(current.children[ch], word, index + 1)
            if should_delete_child:
                del current.children[ch]
                return len(current.children) == 0 and not current.is_end_of_word
            return False
        _delete(self.root, word, 0)

    def search(self, word):
        current = self.root
        for ch in word:
            if ch not in current.children:
                return False
            current = current.children[ch]
        return current.is_end_of_word

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

    def get_all_words_with_freq(self):
        words = []
        
        def _dfs(current, current_prefix=''):
            if current.is_end_of_word:
                words.append((current_prefix, current.frequency))
            for ch, node in current.children.items():
                _dfs(node, current_prefix + ch)
        
        _dfs(self.root)
        return words
    
    def save_keywords_to_file(self, filename):
        words_with_freq = self.get_all_words_with_freq()
        with open(filename, 'w') as f:
            for word, freq in words_with_freq:
                f.write(f'{word},{freq}\n')
    
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




class TrieEditor:
    def __init__(self):
        self.trie = Trie()

    def is_valid_filename(self, filename):
        invalid_chars = set('<>:"/\\|?*')
        return filename and not any(char in invalid_chars for char in filename)

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
    
    def terminate(self):
        print("Exiting the Full Command Prompt . Bye...\n")
        print("Press enter key, to continue...")
        input()
        

    def command_prompt(self, function):
        # Start with an empty Trie
        self.trie = Trie()

        if function == "construct_edit":
            UI.construct_edit()
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
                    self.command_prompt("construct_edit")
                    return  # Restart prompt after showing instructions
                elif cmd == '\\':
                    self.terminate()
                    return
                else:
                    print("Invalid command! Please try again.")
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
                        print(', '.join(f"{word} ({freq})" for word, freq in self.trie.get_words_with_prefix(arg)))
                    elif cmd == '?':
                        if arg:
                            result = self.trie.find_best_match(arg)
                            if result:
                                print(f'Restored word: {result}')
                            else:
                                print("No matching word found.")
                        else:
                            print("Please provide a pattern to match.")

                    elif cmd == '&':
                        print("Invalid command! Please try again.")
                    elif cmd == '@':
                        print("Invalid command! Please try again.")
                    elif cmd == '!':
                        self.command_prompt("predict_restore")
                        return
                    elif cmd == '\\':
                        self.terminate()
                        return
                    else:
                        print("Invalid command! Please try again.")
                        