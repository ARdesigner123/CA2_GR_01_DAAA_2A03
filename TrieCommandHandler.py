from trie import Trie
from user_interface import UserInterface
from TrieVisualiser import TrieVisualizer


UI = UserInterface()

class TrieCommandHandler:
    def __init__(self, trie=None):
        self.trie = trie if trie else Trie()
        self.recent_rounds = []
        self.visualizer = TrieVisualizer(self.trie)

    def get_input(self):
        try:
            raw = input(">> ").strip()
            return raw[0], raw[1:].strip() if len(raw) > 1 else ''
        except EOFError:
            return '\\', ''
        except Exception:
            return '', ''

    def is_valid_filename(self, filename):
        import re
        return not re.search(r'[\\/:*?"<>|]', filename)

    def terminate(self):
        print("Exiting program.")
        exit()

    # Autocomplete game
    def _autoComplete_recursive(self, prefix, guesses):
        suggestions = self.trie.get_words_with_prefix(prefix)
        if not suggestions:
            print("No more suggestions. Ending round.")
            return guesses

        current_guesses = suggestions[:3]
        UI.Game_UI(current_guesses)

        user_input = input("Is the word one of these? Enter number (1-3), or 'n' for none: ").strip().lower()
        if user_input in ['1', '2', '3']:
            chosen_index = int(user_input) - 1
            if chosen_index < len(current_guesses):
                chosen_word = current_guesses[chosen_index]
                print(f"Great! The word is '{chosen_word}'.")
                guesses.append(chosen_word)
                return guesses
            else:
                print(f"Invalid input: only {len(current_guesses)} suggestion(s) shown.")
                return self._autoComplete_recursive(prefix, guesses)

        elif user_input == 'n':
            new_prefix = input("Enter more letters to refine your guess (or just press Enter to stop): ").strip().lower()
            if not new_prefix:
                print("Stopping round.")
                return guesses
            return self._autoComplete_recursive(prefix + new_prefix, guesses)

        else:
            print("Invalid input, try again.")
            return self._autoComplete_recursive(prefix, guesses)

    def _start_autoComplete_round(self):
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
        if not self.recent_rounds:
            print("No recent rounds to review.")
            return

        print("Recent Rounds:")
        for i, (query, guesses) in enumerate(self.recent_rounds[-5:], 1):
            print(f"Round {i}: Query = '{query}'")
            for rank, guess in enumerate(guesses, 1):
                print(f"   {rank}: {guess}")
            print("-" * 50)

    # Main controller
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
                        print("Invalid input! Only letters allowed.")
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
                        print("Invalid input! Only letters allowed.")
                    else:
                        print("Please provide a word to delete.")

                elif cmd == '?':
                    if arg.isalpha():
                        found = self.trie.search(arg)
                        print(f'Keyword "{arg}" is {"present" if found else "not present"}.')
                    elif arg:
                        print("Invalid input! Only letters allowed.")
                    else:
                        print("Please provide a word to search.")

                elif cmd == '@':
                    filename = input("Please enter new filename: ").strip()
                    if filename:
                        self.trie.save_trie_visual(filename)
                        print(f"Trie saved to '{filename}'.")
                    else:
                        print("No filename entered.")

                elif cmd == '~':
                    filename = input("Please enter input file: ").strip()
                    if filename:
                        self.trie = Trie()
                        self.trie.load_keywords_from_file(filename)
                    else:
                        print("No filename entered.")

                elif cmd == '=':
                    if arg and self.is_valid_filename(arg):
                        try:
                            self.trie.save_keywords_to_file(arg)
                            print(f"All keywords written to '{arg}'.")
                        except OSError:
                            print(f"Error: Cannot write to '{arg}'.")
                    else:
                        filename = input("Please enter new filename: ").strip()
                        if filename and self.is_valid_filename(filename):
                            try:
                                self.trie.save_keywords_to_file(filename)
                                print(f"All keywords written to '{filename}'.")
                            except OSError:
                                print(f"Error: Cannot write to '{filename}'.")
                        else:
                            print("Invalid filename.")

                elif cmd == '#':
                    self.trie.display()

                elif cmd == '!':
                    UI.construct_edit(show_empty_trie=False)
                    continue

                elif cmd == '\\':
                    self.terminate()

                else:
                    print("Invalid command! Please try again.")

        elif function == "predict_restore":
            UI.predict_restore()
            while True:
                cmd, arg = self.get_input()
                if not cmd:
                    continue

                if cmd == '~':
                    filename = input("Please enter input file: ").strip()
                    if filename:
                        self.trie.load_keywords_from_file(filename)
                    else:
                        print("No filename entered.")

                elif cmd == '#':
                    self.trie.display()

                elif cmd == '$':
                    arg = input("Please enter input word: ").strip()
                    print(', '.join(f"{word} ({freq})" for word, freq in self.trie.get_words_with_prefix(arg)))

                elif cmd == '?':
                    arg = input("Please enter input word: ").strip()
                    if arg:
                        result = self.trie.find_best_match(arg)
                        print(f'Restored word: {result}' if result else "No matching word found.")
                    else:
                        print("Please provide a pattern to match.")

                elif cmd == '&':
                    arg = input("Enter sentence: ").strip()
                    word_array = self.trie.separate_words(arg)
                    print(self.trie.loop_Sentence_AllMatches(word_array))

                elif cmd == '@':
                    arg = input("Enter sentence: ").strip()
                    word_array = self.trie.separate_words(arg)
                    print(self.trie.loop_Sentence(word_array))

                elif cmd == '!':
                    self.command_prompt("predict_restore")
                    return

                elif cmd == '\\':
                    print("Predicting Restore Function")
                    break

                else:
                    print("Invalid command! Please try again.")

        elif function == "trieChart":
            UI.getTrieChart()
            while True:
                cmd = input("Chart Command: ").strip()

                if cmd == '~':
                    filename = input("Please enter input file: ").strip()
                    if filename:
                        self.trie.load_keywords_from_file(filename)
                    else:
                        print("No filename entered.")

                elif cmd == '^':
                    longest_word = self.visualizer.get_longest_path()
                    print(f"Longest path (word): {longest_word}")
                    self.visualizer.visualize_path(longest_word)

                elif cmd == '!':
                    word = input("Enter word/prefix: ").strip()
                    if word:
                        self.visualizer.visualize_subtree_from_prefix(word)
                    else:
                        print("No word entered.")

                elif cmd == '%':
                    self.visualizer.visualize_frequencies()

                elif cmd == '*':
                    self.visualizer.visualize_structure()

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
                    filename = input("Please enter input file: ").strip()
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
