from feature_base import FeatureBase
import os

class AdvancedTrieFeature(FeatureBase):
    def __init__(self, trie_class):
        self.trie_class = trie_class
        self.trie = self.trie_class()

    def command_prompt(self):
        print("""
------------------------------------------------------------
Advanced Trie Tools - Feature 5 (Aaron Ng)
------------------------------------------------------------
Commands:
    ~file1,file2    Load and merge two Trie keyword files into one
    >file.txt       Show top 5 keywords (by frequency) from a file
    ^old,new        Replace 'old' keyword with 'new' in current Trie
    !               Print instructions again
    \               Exit to main menu
------------------------------------------------------------
        """)

        while True:
            print("[Feature 5] > ", end='')
            user_input = input().strip()

            if not user_input:
                continue

            command = user_input[0]
            args = user_input[1:].strip()

            if command == '~':
                self.load_and_merge_files(args)

            elif command == '>':
                self.display_top_5(args)

            elif command == '^':
                self.replace_word(args)

            elif command == '!':
                self.command_prompt()
                return

            elif command == '\\':
                print("Exiting Feature 5: Advanced Trie Tools. Returning to main menu...")
                break

            else:
                print("Invalid command. Use ! to see instructions.")

    def run(self):
        self.command_prompt()

    def load_and_merge_files(self, arg):
        if ',' not in arg:
            print("Invalid format. Use: ~file1.txt,file2.txt")
            return

        file1, file2 = map(str.strip, arg.split(',', 1))

        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"One or both files '{file1}', '{file2}' do not exist.")
            return

        print(f"Merging tries from '{file1}' and '{file2}'...")

        self.trie = self.trie_class()  # Reset current trie
        self.trie.load_keywords_from_file(file1)
        self.trie.load_keywords_from_file(file2)

        print("Merge complete. Displaying merged trie:")
        self.trie.display()

    def display_top_5(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return

        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)

        all_words = temp_trie.get_all_words_with_freq()
        top_5 = sorted(all_words, key=lambda x: x[1], reverse=True)[:5]

        print("Top 5 keywords by frequency:")
        for word, freq in top_5:
            print(f" - {word}: {freq}")

    def replace_word(self, args):
        if ',' not in args:
            print("Invalid format. Use: ^oldword,newword")
            return

        old, new = map(str.strip, args.split(',', 1))

        if not self.trie.search(old):
            print(f"'{old}' not found in current Trie.")
            return

        freq = 1
        for word, f in self.trie.get_all_words_with_freq():
            if word == old:
                freq = f
                break

        self.trie.delete(old)
        for _ in range(freq):
            self.trie.insert(new)

        print(f"'{old}' has been replaced with '{new}' (with frequency {freq}).")