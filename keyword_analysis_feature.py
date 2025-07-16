from feature_base import FeatureBase
import os

class KeywordAnalysisFeature(FeatureBase):
    def __init__(self, trie_class):
        self.trie_class = trie_class
        self.trie1 = self.trie_class()
        self.trie2 = self.trie_class()

    def run(self):
        self.command_prompt()

    def print_instructions(self):
        print("----------------------------------------------------------------------")
        print("Extra Feature Two - Keyword Tools (Aaron Ng)")
        print("----------------------------------------------------------------------")
        print("    =file1,file2   (Compare common keywords in both TXT files)")
        print("    >from,to       (Transfer a keyword from one TXT file to another)")
        print("    #file.txt      (Show keywords from longest to shortest)")
        print("    *file.txt      (Group keywords alphabetically by first letter)")
        print(f"    %file.txt      (Show most frequent starting letters)")
        print("    $file.txt      (List palindromic keywords)")
        print("    !              (Print instructions again)")
        print("    \\              (Exit this feature)")
        print("----------------------------------------------------------------------")

    def command_prompt(self):
        self.print_instructions()
        while True:
            print("[Extra Feature 2] > ", end='')
            user_input = input().strip()

            if not user_input:
                continue

            command = user_input[0]
            args = user_input[1:].strip()

            if command == '=':
                self.compare_keywords(args)
            elif command == '>':
                self.transfer_keyword(args)
            elif command == '#':
                self.sort_keywords_by_length(args)
            elif command == '*':
                self.group_by_alphabet(args)
            elif command == '%':
                self.top_starting_letters(args)
            elif command == '$':
                self.find_palindromes(args)
            elif command == '!':
                self.print_instructions()
            elif command == '\\':
                print("Exiting Extra Feature Two: Keyword Tools.")
                break
            else:
                print("Invalid command. Use ! to see instructions.")

    def compare_keywords(self, arg):
        if ',' not in arg:
            print("Invalid format. Use: =file1.txt,file2.txt")
            return

        file1, file2 = map(str.strip, arg.split(',', 1))

        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"One or both files '{file1}', '{file2}' do not exist.")
            return

        trie1 = self.trie_class()
        trie1.load_keywords_from_file(file1)
        words1 = set(w for w, _ in trie1.get_all_words_with_freq())

        trie2 = self.trie_class()
        trie2.load_keywords_from_file(file2)
        words2 = set(w for w, _ in trie2.get_all_words_with_freq())

        common = words1.intersection(words2)

        if not common:
            print("No common keywords found.")
        else:
            print("Common keywords:")
            for word in sorted(common):
                print(f" - {word}")

    def transfer_keyword(self, arg):
        if ',' not in arg:
            print("Invalid format. Use: >from.txt,to.txt")
            return
        
        file1, file2 = map(str.strip, arg.split(',', 1))
        
        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"One or both files '{file1}', '{file2}' do not exist.")
            return
        
        self.trie1 = self.trie_class()
        self.trie2 = self.trie_class()
        self.trie1.load_keywords_from_file(file1)
        self.trie2.load_keywords_from_file(file2)
        
        while True:
            print("Enter keyword to transfer from first file to second: ", end='')
            word = input().strip()
            
            all_words = dict(self.trie1.get_all_words_with_freq())
            if word not in all_words:
                print(f"'{word}' not found in '{file1}'.")
                continue
            
            # Transfer only ONE instance
            self.trie1.delete(word)
            self.trie2.insert(word)
            
            print(f"'{word}' transferred from '{file1}' to '{file2}'.")
            
            print("\nUpdated Trie for first file:")
            self.trie1.display()
            
            print("\nUpdated Trie for second file:")
            self.trie2.display()
            
            print("\nDo you want to transfer another keyword? (yes/no): ", end='')
            again = input().strip().lower()
            if again != 'yes':
                break
            
        print("\nDo you want to save updates to both TXT files? (yes/no): ", end='')
        save = input().strip().lower()
        if save == 'yes':
            self.trie1.save_keywords_to_file(file1)
            self.trie2.save_keywords_to_file(file2)
            print("Changes saved.")
        else:
            print("Changes were not saved.")

    def sort_keywords_by_length(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return

        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)
        all_words = temp_trie.get_all_words_with_freq()
        sorted_words = sorted(all_words, key=lambda x: (-len(x[0]), x[0]))

        print("\nKeywords from longest to shortest:")
        for word, freq in sorted_words:
            print(f" - {word} ({freq})")
    
    def group_by_alphabet(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)
        all_words = temp_trie.get_all_words_with_freq()
        
        grouped = {}
        for word, freq in all_words:
            first_letter = word[0].upper()
            if not first_letter.isalpha():
                first_letter = '#'  # for non-alphabet characters
            grouped.setdefault(first_letter, []).append((word, freq))
        
        print(f"\nGrouped keywords in '{filename}':")
        for letter in sorted(grouped.keys()):
            print(f"\n{letter}:")
            for word, freq in sorted(grouped[letter]):
                print(f"  - {word} ({freq})")

    def top_starting_letters(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)
        all_words = temp_trie.get_all_words_with_freq()
        
        letter_counts = {}
        for word, _ in all_words:
            first_letter = word[0].upper()
            if not first_letter.isalpha():
                first_letter = '#'
            letter_counts[first_letter] = letter_counts.get(first_letter, 0) + 1
        
        sorted_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print(f"\nTop starting letters in '{filename}':")
        for letter, count in sorted_letters:
            print(f"  - {letter}: {count} words")
    
    def find_palindromes(self, filename):
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)
        all_words = temp_trie.get_all_words_with_freq()
        
        palindromes = [(word, freq) for word, freq in all_words if word == word[::-1] and len(word) > 1]
        
        if not palindromes:
            print(f"No palindromic keywords found in '{filename}'.")
        else:
            print(f"\nPalindromic keywords in '{filename}':")
            for word, freq in sorted(palindromes):
                print(f"  - {word} ({freq})")