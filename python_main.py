# Group members info
group_members = [
    "Stephen Bermudo (2442657)",
    "Aaron Ng (2442631)"
]

# Import required classes from other modules
from trie import Trie
from trie_editor import TrieEditor
from TrieCommandHandler import TrieCommandHandler
from feature_advanced_editor import AdvancedTrieFeature
from user_interface import UserInterface
from keyword_analysis_feature import KeywordAnalysisFeature
    
# ---------------------------
# Main program loop (Done by Aaron)
# ---------------------------
def main():# Create User Interface and Trie Editor instances
    trie_instance = Trie()
    TCH = TrieCommandHandler()  
    UI = UserInterface()

    # Display welcome banner once at the start
    UI.print_banner()

    # Main menu loop
    while True:
        UI.display_menu()
        choice = input("Enter choice: ").strip()
        
        # ---------------------------
        # Option 1: Construct/Edit Trie (Done by Aaron)
        # ---------------------------
        if choice == '1': 
            print("You selected Option 1: Construct/Edit Trie\n")
            TCH.command_prompt("construct_edit")
        
        # ---------------------------
        # Option 2: Predict/Restore Text (Done by Stephen)
        # ---------------------------
        elif choice == '2':
            print("You selected Option 2: Predict/Restore Text\n")
            TCH.command_prompt("predict_restore")
        
        # ---------------------------
        # Extra Feature One (To be implemented by Stephen)
        # ---------------------------
        elif choice == '3':
            print("You selected Trie Charter (Stephen Bermudo)\n")
            TCH.command_prompt("trieChart")
        # ---------------------------
        # Extra Feature Two (To be implemented by Stephen)
        # ---------------------------
        elif choice == '4':
            print("You selected Inbuilt Analytics (Stephen Bermudo)\n")
            TCH.command_prompt("autoComplete")
        
        # ---------------------------
        # Option 5: Advanced Trie Tools (Done by Aaron)
        # ---------------------------
        elif choice == '5':
            print("You selected Option 5: Advanced Trie Tools (Aaron Ng)\n")
            feature5 = AdvancedTrieFeature(trie_instance)
            feature5.run()
        
        # ---------------------------
        # Option 6: Keyword Analysis Feature (Done by Aaron)
        # ---------------------------
        elif choice == '6':
            print("You selected Option 6: Keyword Analysis Feature (Aaron Ng)\n")
            feature6 = KeywordAnalysisFeature(trie_instance)
            feature6.run()
        
        # ---------------------------
        # Option 7: Exit the program
        # ---------------------------
        elif choice == '7':
            print("Exiting the program. Goodbye!\n")
            break
        
        # ---------------------------
        # Handle invalid menu input
        # ---------------------------
        else:
            print("Invalid choice! Please enter a number from 1 to 7.\n")

# Start the main program
if __name__ == "__main__":
    main()