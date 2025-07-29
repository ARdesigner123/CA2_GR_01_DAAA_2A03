class AutoCompleteGame:
    def __init__(self, trie, ui_module):
        self.trie = trie
        self.UI = ui_module  # expects UI.Game_UI() method
        self.recent_rounds = []

    def _autoComplete_recursive(self, prefix, guesses):
        suggestions = self.trie.get_words_with_prefix(prefix)
        if not suggestions:
            print("No more suggestions. Ending round.")
            return guesses

        # Take up to 3 suggestions to show
        current_guesses = suggestions[:3]
        self.UI.Game_UI(current_guesses)

        # Ask user if any guess is correct
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

    def run(self):
        print("== Autocomplete Game ==")
        while True:
            print("\nMenu:")
            print("1. Start new round")
            print("2. Review recent rounds")
            print("3. Exit")
            choice = input("Choose an option: ").strip()

            if choice == '1':
                self._start_autoComplete_round()
            elif choice == '2':
                self._review_recent_rounds()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
