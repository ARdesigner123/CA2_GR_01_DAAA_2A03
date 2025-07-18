# ----------------------------------------
# feature_advanced_editor.py
# Advanced Trie Tools Implementation
# Done By Aaron
# ----------------------------------------

from feature_base import FeatureBase
import os

class AdvancedTrieFeature(FeatureBase):
    def __init__(self, trie_class):
        # Store the Trie class reference and create a new Trie instance
        self.trie_class = trie_class
        self.trie = self.trie_class()

    def command_prompt(self):
        # Display feature banner and command instructions
        print("----------------------------------------------------------------------")
        print("Advanced Trie Tools - Feature 5 (Aaron Ng)")
        print("----------------------------------------------------------------------")
        print("    ~file1,file2    (load and merge two Trie keyword files into one)")
        print("    >file.txt       (show top keywords by frequency from a file)")
        print("    +               (add a keyword to a TXT file and update Trie)")
        print("    -               (remove a keyword from a TXT file and update Trie)")
        print("    ^               (replace 'old' keyword with 'new' in current Trie)")
        print("    !               (print instructions again)")
        print("    \\               (exit)")
        print("----------------------------------------------------------------------")

        # Main loop to handle user input commands
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
                self.display_top(args)
            
            elif command == '+':
                self.increment_keyword()
            
            elif command == '-':
                self.decrement_keyword()

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
        # Run this feature through the command prompt
        self.command_prompt()

    def load_and_merge_files(self, arg):
        # Parse filenames and check format
        if ',' not in arg:
            print("Invalid format. Use: ~file1.txt,file2.txt")
            return
        
        file1, file2 = map(str.strip, arg.split(',', 1))
        
        # Check file existence
        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"One or both files '{file1}', '{file2}' do not exist.")
            return
        
        print(f"Merging tries from '{file1}' and '{file2}'...")

        # Reset and load both Tries
        self.trie = self.trie_class()  # Reset current trie
        self.trie.load_keywords_from_file(file1)
        self.trie.load_keywords_from_file(file2)
        
        print("Merge complete. Displaying merged trie:")
        self.trie.display()
        
        # Ask to save merged Trie
        print("\nDo you want to save the merged Trie to a new TXT file? (yes/no): ", end='')
        save = input().strip().lower()
        
        if save == 'yes':
            print("Enter filename to save the merged Trie (e.g., merged.txt): ", end='')
            save_filename = input().strip()
            
            if save_filename == '':
                print("Invalid filename. Merged Trie not saved.")
                return
            
            self.trie.save_keywords_to_file(save_filename)
            print(f"Merged Trie has been saved to '{save_filename}'.")
        else:
            print("Merged Trie was not saved.")

    def display_top(self, filename):
        # Load file and build a temporary Trie
        if not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        temp_trie = self.trie_class()
        temp_trie.load_keywords_from_file(filename)
        
        all_words = temp_trie.get_all_words_with_freq()
        if not all_words:
            print(f"No keywords found in '{filename}'.")
            return
        
        # Ask user for number of top keywords
        while True:
            print("Enter how many top keywords to display (e.g., 5): ", end='')
            try:
                top_n = int(input().strip())
                if top_n <= 0:
                    print("Please enter a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid number. Please enter a valid integer.")
        
        # Sort by frequency descending
        top_n_keywords = sorted(all_words, key=lambda x: x[1], reverse=True)[:top_n]
        
        print(f"\nTop {top_n} keywords by frequency:")
        for word, freq in top_n_keywords:
            print(f" - {word}: {freq}")
    
    def increment_keyword(self):
        # Add new keyword(s) to the file and Trie
        print("Enter filename to load the Trie from: ", end='')
        filename = input().strip()
        
        if not filename or not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        self.trie = self.trie_class()
        self.trie.load_keywords_from_file(filename)
        
        while True:
            print("Enter +keyword to add (e.g., +cat): ", end='')
            user_input = input().strip()
            if not user_input.startswith('+') or len(user_input) <= 1:
                print("Invalid format. Use: +keyword")
                continue
            
            keyword = user_input[1:].strip()
            if not keyword:
                print("Keyword cannot be empty.")
                continue
            
            self.trie.insert(keyword)
            print(f"'{keyword}' has been added to the Trie (frequency increased by 1).")
            
            print("\nUpdated Trie structure:")
            self.trie.display()
            
            print("\nDo you want to add another keyword? (yes/no): ", end='')
            again = input().strip().lower()
            if again != 'yes':
                break
        
        # Ask to save
        print("\nDo you want to update and save the TXT file? (yes/no): ", end='')
        save_choice = input().strip().lower()
        if save_choice == 'yes':
            self.trie.save_keywords_to_file(filename)
            print(f"Trie has been saved to '{filename}'.")
        else:
            print("Changes were not saved.")
    
    def decrement_keyword(self):
        # Remove keyword(s) from the file and Trie
        print("Enter filename to load the Trie from: ", end='')
        filename = input().strip()
        
        if not filename or not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        self.trie = self.trie_class()
        self.trie.load_keywords_from_file(filename)
        
        while True:
            print("Enter -keyword to subtract (e.g., -cat): ", end='')
            user_input = input().strip()
            if not user_input.startswith('-') or len(user_input) <= 1:
                print("Invalid format. Use: -keyword")
                continue
            
            keyword = user_input[1:].strip()
            if not keyword:
                print("Keyword cannot be empty.")
                continue
            
            all_words = dict(self.trie.get_all_words_with_freq())
            if keyword not in all_words:
                print(f"'{keyword}' not found in the Trie.")
                continue
            
            self.trie.delete(keyword)
            print(f"One occurrence of '{keyword}' has been removed from the Trie.")
            
            print("\nUpdated Trie structure:")
            self.trie.display()
            
            print("\nDo you want to subtract another keyword? (yes/no): ", end='')
            again = input().strip().lower()
            if again != 'yes':
                break
        
        # Ask to save
        print("\nDo you want to update and save the TXT file? (yes/no): ", end='')
        save_choice = input().strip().lower()
        if save_choice == 'yes':
            self.trie.save_keywords_to_file(filename)
            print(f"Trie has been saved to '{filename}'.")
        else:
            print("Changes were not saved.")

    def replace_word(self, args):
        # Replace old keyword with new one in the file
        print("Enter filename to load the Trie from: ", end='')
        filename = input().strip()
        
        if not filename or not os.path.exists(filename):
            print(f"File '{filename}' not found.")
            return
        
        self.trie = self.trie_class()
        self.trie.load_keywords_from_file(filename)
        
        while True:
            # Step 1: Show current words
            print("\nCurrent keywords with frequencies:")
            all_words = self.trie.get_all_words_with_freq()
            for word, freq in sorted(all_words):
                print(f"{word},{freq}")
            
            print("\nEnter ^old,new to replace a word: ", end='')
            replace_input = input().strip()
            if not replace_input.startswith('^') or ',' not in replace_input:
                print("Invalid format. Use: ^oldword,newword")
                return
            
            old, new = map(str.strip, replace_input[1:].split(',', 1))
            
            # Step 2: Find and replace word in the list
            new_word_list = []
            replaced = False
            freq_to_add = 0
            
            for word, freq in all_words:
                if word == old:
                    freq_to_add = freq
                    replaced = True
                else:
                    new_word_list.append((word, freq))
            
            if not replaced:
                print(f"'{old}' not found in current Trie.")
                continue
            
            new_word_list.append((new, freq_to_add))
            
            # Step 3: Rebuild Trie
            self.trie = self.trie_class()
            for word, freq in new_word_list:
                for _ in range(freq):
                    self.trie.insert(word)
            
            print(f"\n'{old}' has been replaced with '{new}' (with frequency {freq_to_add}).")
            
            # Step 4: Show updated Trie
            print("\nUpdated Trie structure:")
            self.trie.display()
            
            # Step 5: Ask if want to replace more
            print("\nDo you want to replace another keyword? (yes/no): ", end='')
            again = input().strip().lower()
            if again != 'yes':
                break
        
        # Step 6: Ask to save
        print("\nDo you want to update and save the TXT file? (yes/no): ", end='')
        save_choice = input().strip().lower()
        if save_choice == 'yes':
            self.trie.save_keywords_to_file(filename)
            print(f"Trie has been saved to '{filename}'.")
        else:
            print("Changes were not saved.")