from trie import Trie
from user_interface import UserInterface

UI = UserInterface()

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

                        