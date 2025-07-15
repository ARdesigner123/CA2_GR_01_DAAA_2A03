# Group members info
group_members = [
    "Stephen Bermudo (2442657)",
    "Aaron Ng (2442631)"
]

from trie_editor import TrieEditor, Trie
from feature_advanced_editor import AdvancedTrieFeature
from user_interface import UserInterface
    
# Main program loop
def main():
    UI = UserInterface()
    trie_editor = TrieEditor()
    UI.print_banner()  # Show banner only once

    while True:
        UI.display_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            print("You selected Option 1: Construct/Edit Trie\n")
            trie_editor.command_prompt("construct_edit")
        elif choice == '2':
            print("You selected Option 2: Predict/Restore Text\n")
            trie_editor.command_prompt("predict_restore")
        elif choice == '3':
            print("You selected Extra Feature One (Stephen Bermudo)\n")
            # Call your function here
        elif choice == '4':
            print("You selected Extra Feature Two (Stephen Bermudo)\n")
            # Call your function here
        elif choice == '5':
            print("You selected Option 5: Advanced Trie Tools (Aaron Ng)\n")
            feature5 = AdvancedTrieFeature(Trie)
            feature5.run()
        elif choice == '6':
            print("You selected Extra Feature Two (Aaron Ng)\n")
            # Call your function here
        elif choice == '7':
            print("Exiting the program. Goodbye!\n")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 7.\n")

if __name__ == "__main__":
    main()